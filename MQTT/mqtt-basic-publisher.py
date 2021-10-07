#!/usr/bin/python

import paho.mqtt.publish as publish
import sys

# Note : The idea is to generate a single mqtt message using three types of data 1. broker address 2. mqtt topic 3. content

MQTT_SERVER= sys.argv[1] # can be localhost 
MQTT_PATH= sys.argv[2] # corresponds to the topic
message= sys.argv[3] # corresponds to the topic

publish.single(MQTT_PATH,message,hostname=MQTT_SERVER)


