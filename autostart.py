import boto3

def lambda_handler(event, context):
    ec2 = boto3.client('ec2', region_name='regiao-aws')

    # Filtra instâncias com a tag 'AutoStart' = 'True'
    # Você pode usar a mesma tag 'AutoStop' = 'True' e filtrar por 'stopped'
    filters = [{
            'Name': 'tag:AutoStart', # Ou 'AutoStop' se preferir usar a mesma tag
            'Values': ['True']
        },
        {
            'Name': 'instance-state-name',
            'Values': ['stopped']
        }
    ]

    instances = ec2.describe_instances(Filters=filters)

    instances_to_start = []
    for reservation in instances['Reservations']:
        for instance in reservation['Instances']:
            instances_to_start.append(instance['InstanceId'])

    if instances_to_start:
        print(f"Ligando as seguintes instâncias: {instances_to_start}")
        ec2.start_instances(InstanceIds=instances_to_start)
    else:
        print("Nenhuma instância para ligar encontrada.")

    return {
        'statusCode': 200,
        'body': 'Função de ligamento executada com sucesso!'
    }