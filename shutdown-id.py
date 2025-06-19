import boto3
import json

def lambda_handler(event, context):
    # --- Configurações ---
    # Substitua pela sua região AWS (ex: 'sa-east-1')
    AWS_REGION = 'sua-regiao-aws'
    # --- Fim das Configurações ---

    ec2 = boto3.client('ec2', region_name=AWS_REGION)

    # Tenta obter os IDs das instâncias do evento.
    # Esperamos que o JSON do EventBridge tenha uma chave 'instance_ids'.
    # Ex: {"instance_ids": ["i-1234567890abcdef0", "i-fedcba09876543210"]}
    INSTANCE_IDS_TO_STOP = event.get('instance_ids', [])

    if not INSTANCE_IDS_TO_STOP:
        print("Nenhum ID de instância fornecido no evento de entrada para desligar.")
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
        print(f"Erro ao descrever instâncias: {e}. Alguns IDs podem não ter sido encontrados.")
        # Se algum ID não for encontrado, ele será ignorado na lista de running_instances
        pass
        
    if running_instances:
        print(f"Tentando desligar as seguintes instâncias: {running_instances}")
        try:
            ec2.stop_instances(InstanceIds=running_instances)
            print("Solicitação de desligamento enviada com sucesso para as instâncias especificadas.")
        except ec2.exceptions.ClientError as e:
            print(f"Erro ao desligar instâncias: {e}")
            # Você pode adicionar lógica de tratamento de erro mais específica aqui
    else:
        print("Nenhuma das instâncias especificadas no evento está em estado 'running' para ser desligada.")

    return {
        'statusCode': 200,
        'body': 'Processo de desligamento por ID concluído.'
    }