import boto3

def lambda_handler(event, context):
    ec2 = boto3.client('ec2', region_name='sa-east-1') 

    # Filtra instâncias com a tag 'AutoStop' = 'True'
    filters = [{
            'Name': 'tag:AutoStop',
            'Values': ['True']
        },
        {
            'Name': 'instance-state-name',
            'Values': ['running']
        }
    ]

    instances = ec2.describe_instances(Filters=filters)

    instances_to_stop = []
    for reservation in instances['Reservations']:
        for instance in reservation['Instances']:
            instances_to_stop.append(instance['InstanceId'])

    if instances_to_stop:
        print(f"Desligando as seguintes instâncias: {instances_to_stop}")
        ec2.stop_instances(InstanceIds=instances_to_stop)
    else:
        print("Nenhuma instância para desligar encontrada.")

    return {
        'statusCode': 200,
        'body': 'Função de desligamento executada com sucesso!'
    }