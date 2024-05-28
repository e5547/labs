from paho.mqtt import client as mqtt_client
import random
import time 

broker = 'broker.hivemq.com'
port = 1883
topic = "lab3_posuidexin"
client_id = f'python-mqtt-{random.randint(0, 1000)}'

def connect_mqtt():
    def on_connect(client, userdata, flags, rc, properties):
        if rc == 0:
            print("Connected to MQTT Broker!")
        else:
            print("Failed to connect, return code %d\n", rc)

    client = mqtt_client.Client(client_id=client_id, callback_api_version=mqtt_client.CallbackAPIVersion.VERSION2)

    
    client.on_connect = on_connect
    client.connect(broker, port)
    return client



def publish(client):
    time.sleep(1)
    msg = f"Lab3 is done!"
    result = client.publish(topic, msg)
   
    status = result[0]
    if status == 0:
        print(f"Send `{msg}` to topic `{topic}`")
    else:
        print(f"Failed to send message to topic {topic}")
    


def run():
    client = connect_mqtt()
    client.loop_start()
    publish(client)
    client.loop_stop()


if __name__ == '__main__':
    run()

