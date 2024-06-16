import yaml
import docker

def serve():
    # read configuration file to get all parameters
    with open('config.yaml') as fp:
        config = yaml.safe_load(fp)
    fp.close()
    
    # start name server
    redis_image = config['name_server']['image']
    redis_name = config['name_server']['name']
    redis_ip = config['name_server']['ip']
    redis_port = config['name_server']['port']

    # start from docker
    client = docker.from_env()
    try:
        redis_container = client.containers.get(redis_name)
        redis_container.start()
    except:
        container_conf = {  'image': f'{redis_image}',
                            'name': f'{redis_name}',
                            'detach': True, # background execution, on bash a simple '&' at the end would do, 
                                            # but I prefer having full control over the process programatically
                            'ports': {f'{redis_port}/tcp': (f'{redis_ip}', redis_port)} }
        redis_container = client.containers.run(**container_conf)

    # start the broker (same as for redis)
    rabbit_image = config['broker']['image']
    rabbit_name = config['broker']['name']
    rabbit_ip = config['broker']['ip']
    rabbit_port = config['broker']['port']
    rabbit_http = config['broker']['http']

    # docker configuration and start
    try:
        rabbit_container = client.containers.get(rabbit_name)
        rabbit_container.start()
    except:
        container_conf = {  'image': f'{rabbit_image}',
                            'name': f'{rabbit_name}',
                            'detach': True, # background execution, on bash a simple '&' at the end would do, 
                                            # but I prefer having full control over the process programatically
                            'ports': {f'{rabbit_port}/tcp': (f'{rabbit_ip}', rabbit_port), f'{rabbit_http}/tcp': (f'{rabbit_ip}', rabbit_http)} }
        rabbit_container = client.containers.run(**container_conf)




if __name__ == '__main__':
    serve()