import requests

def get_connectors(kafka_connect_url):
    response = requests.get(f"http://{kafka_connect_url}/connectors")
    if (response.ok):
        return(response.json())
    else:
        raise Exception(response.text)


def get_connector_details(kafka_connect_url, connector_name):
    response = requests.get(f"http://{kafka_connect_url}/connectors/{connector_name}")
    if (response.ok):
        return(response.json())
    else:
        raise Exception(response.text)
        
def create_tumbersome_command(connector_name,server_name, kafka_server, connect_offset_topic ):
        command=f"""echo '["{connector_name}",""" +  \
        """ {"server": """  +  \
        """ "{}" """.format(server_name) + \
        """}]|'""" + \
        """ | {} -P -Z -b {} -t {} -K \| -p 11""".format(kafkacat, kafka_server, connect_offset_topic)
        print(f"before executing:  {command}")
        return(command)

import os
kafkacat=os.getenv('KAFKACAT_COMMAND', default = '/usr/local/bin/kcat')
kafka_servers=os.getenv('BROKER_LIST', default = 'localhost:9092')
kafka_server=kafka_servers.split(',')[0]
kafka_connect_url=os.getenv('CONNECT_CLUSTER', default = 'localhost:8083')
connect_offset_topic=os.getenv('CONNECT_OFFSET_TOPIC', default = 'docker-connect-offsets')
connectors_list=get_connectors(kafka_connect_url)
if (len(connectors_list)==0):
    print('no connectors defined for the cluster')
connector_details_list=[]
for connector_name in connectors_list:
    connector_details=get_connector_details(kafka_connect_url, connector_name)
    connector_details_list.append(connector_details)
for i in connector_details_list:
    if ('debezium' in (i['config']['connector.class'])):
        connector_name=i['name']
        server_name=i['config']['database.server.name']
        command=create_tumbersome_command(connector_name, server_name, kafka_server, connect_offset_topic)
        stat=os.system(command)
        if (stat==0):
            print(f"tumbstone command for connector {connector_name} succeded")
        else:
            raise Exception(f"tumbstone command for connector {connector_name} failed")