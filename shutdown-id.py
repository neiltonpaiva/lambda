import boto3

def lambda_handler(event, context):
    # --- Configurações ---
    # Substitua pela sua região AWS (ex: 'sa-east-1')
    AWS_REGION = 'sua-regiao-aws'
    
    # Lista de IDs das instâncias EC2 que você deseja desligar.
    # Ex: INSTANCE_IDS_TO_STOP = ['i-1234567890abcdef0', 'i-fedcba09876543210']
    # Para customizações, você pode passar esses IDs no 'event' da Lambda ou como variável de ambiente.
    INSTANCE_IDS_TO_STOP = [
        'ID_DA_SUA_INSTANCIA_1',
        'ID_DA_SUA_INSTANCIA_2',
        # Adicione mais IDs conforme necessário
    ]
    # --- Fim das Configurações ---

    ec2 = boto3.client('ec2', region_name=AWS_REGION)

    if not INSTANCE_IDS_TO_STOP:
        print("Nenhum ID de instância fornecido para desligar.")
        return {
            'statusCode': 200,
            'body': 'Nenhuma instância para desligar.'
        }

    # Verifica o estado atual das instâncias antes de tentar desligá-las
    running_instances = []
    try:
        response = ec2.describe_instances(InstanceIds=INSTANCE_IDS_TO_STOP,
                                         Filters=[{'Name': 'instance-state-name', 'Values': ['running']}])
        for reservation in response['Reservations']:
            for instance in reservation['Instances']:
                running_instances.append(instance['InstanceId'])
    except ec2.exceptions.ClientError as e:
        print(f"Erro ao descrever instâncias: {e}")
        # Se algum ID não for encontrado, ele será ignorado na lista de running_instances
        # Mas a função pode continuar tentando desligar os que foram encontrados
        pass
        
    if running_instances:
        print(f"Tentando desligar as seguintes instâncias: {running_instances}")
        try:
            ec2.stop_instances(InstanceIds=running_instances)
            print("Solicitação de desligamento enviada com sucesso para as instâncias especificadas.")
        except ec2.exceptions.ClientError as e:
            print(f"Erro ao desligar instâncias: {e}")
            # Você pode adicionar lógica de tratamento de erro mais específica aqui
            # Ex: permissões insuficientes, instância já em estado 'stopping'
    else:
        print("Nenhuma das instâncias especificadas está em estado 'running' para ser desligada.")

    return {
        'statusCode': 200,
        'body': 'Processo de desligamento por ID concluído.'
    }

# Exemplo de como você chamaria a função se estivesse testando localmente (fora da Lambda)
# if __name__ == "__main__":
#     # Defina seu 'event' e 'context' de teste, se necessário
#     test_event = {} 
#     test_context = {}
#     lambda_handler(test_event, test_context)