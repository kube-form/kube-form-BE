
import boto3,yaml,os
client = boto3.client('s3')

def download_dir(client, resource, dist, local, bucket):
    paginator = client.get_paginator('list_objects')
    for result in paginator.paginate(Bucket=bucket, Delimiter='/', Prefix=dist):
        if result.get('CommonPrefixes') is not None:
            for subdir in result.get('CommonPrefixes'):
                download_dir(client, resource, subdir.get('Prefix'), local, bucket)
        for file in result.get('Contents', []):
            dest_pathname = os.path.join(local, file.get('Key'))
            if not os.path.exists(os.path.dirname(dest_pathname)):
                os.makedirs(os.path.dirname(dest_pathname))
            if not file.get('Key').endswith('/'):
                print(dest_pathname)
                resource.meta.client.download_file(bucket, file.get('Key'), dest_pathname)



def make_yaml(params) :

    with open('.././sample/namespace.yaml') as f:
        namespace_yaml = yaml.load(f, Loader=yaml.FullLoader)
    
    namespace_yaml['metadata']['name'] = params['user_id'] + '-ns'
    namespace_yaml['metadata']['labels']['name'] = params['user_id'] + '-ns'

    with open(f".././k8s/anamespace-{params['user_id']}.yaml", 'w') as file:
        yaml.dump(namespace_yaml, file, default_flow_style=False)
    
    for c in params['container']:
        ##deployment
        with open('.././sample/deployment.yaml') as f:
            deployment_yaml = yaml.load(f, Loader=yaml.FullLoader)
        print("test")
        deployment_yaml['metadata']['name'] = c['name']
        deployment_yaml['metadata']['namespace'] = params['user_id'] + '-ns'
        deployment_yaml['spec']['replicas'] = c['replicas']
        deployment_yaml['spec']['selector']['matchLabels']['app'] = c['name'] + '-label'
        deployment_yaml['spec']['template']['metadata']['labels']['app'] = c['name'] + '-label'
        deployment_yaml['spec']['template']['spec']['containers'][0]['name'] = c['name']
        deployment_yaml['spec']['template']['spec']['containers'][0]['image'] = c['dockerURL']
        deployment_yaml['spec']['template']['spec']['containers'][0]['ports'][0]['containerPort'] = c['port']

        with open(f".././k8s/deployment-{c['name']}.yaml", 'w') as file:
            yaml.dump(deployment_yaml, file, default_flow_style=False)
        ##service
        with open('.././sample/service.yaml') as f:
            service_yaml = yaml.load(f, Loader=yaml.FullLoader)
        
        service_yaml['metadata']['name'] = c['name'] + '-nlb'
        service_yaml['metadata']['namespace']= params['user_id'] + '-ns'
        service_yaml['spec']['selector']['app'] = c['name'] + '-label'

        with open(f".././k8s/service-{c['name']}.yaml", 'w') as file:
            yaml.dump(service_yaml, file, default_flow_style=False)
        


