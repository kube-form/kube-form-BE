import yaml

def f() : 
    for c in params['container']:
        with open('.././sample/deployment.yaml') as f:
            deployment_yaml = yaml.load(f, Loader=yaml.FullLoader)

        deployment_yaml['metadata']['name'] = c['name']
        deployment_yaml['spec']['replicas'] = c['replicas']
        deployment_yaml['spec']['selector']['matchLabels']['app'] = c['name'] + '_label'
        deployment_yaml['spec']['template']['metadata']['labels']['app'] = c['name'] + '_label'
        deployment_yaml['spec']['template']['spec']['containers'][0]['name'] = c['name']
        deployment_yaml['spec']['template']['spec']['containers'][0]['image'] = c['dockerURL']
        deployment_yaml['spec']['template']['spec']['containers'][0]['ports'][0]['containerPort'] = c['port']

        with open(f".././k8s/deployment-{c['name']}.yaml", 'w') as file:
            yaml.dump(deployment_yaml, file, default_flow_style=False)
        
        with open('.././sample/service.yaml') as f:
            service_yaml = yaml.load(f, Loader=yaml.FullLoader)
        
        service_yaml['metadata']['name'] = c['name'] + '_nlb'
        service_yaml['spec']['selector'] = c['name'] + '_label'
        service_yaml['spec']['ports'][0]['port'] = c['port']

        with open(f".././k8s/service-{c['name']}.yaml", 'w') as file:
            yaml.dump(service_yaml, file, default_flow_style=False)