import paho.mqtt.client as mqtt

MQTT_PATH="test-message-mqtt"
MQTT_SERVER="localhost"

def on_connect(client,userdata,flags,rc):
    client.subscribe(MQTT_PATH)
    
def on_message(client,userdata,msg):
    print("Subject: " +msg.topic+ "Message: "+str(msg.payload))
    
def on_log(client,userdata,level,buf):
    print("log: ",buf)

client=mqtt.Client()
client.on_connect=on_connect
client.on_message=on_message
client.on_log=on_log
client.connect(MQTT_SERVER, 1883, 60)

client.loop_forever()
