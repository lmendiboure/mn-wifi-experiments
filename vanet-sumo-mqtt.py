#!/usr/bin/python

"""Sample file for SUMO

***Requirements***:

Kernel version: 5.8+ (due to the 802.11p support)
sumo 1.5.0 or higher
sumo-gui"""

import os

from mininet.log import setLogLevel, info
from mn_wifi.cli import CLI
from mn_wifi.net import Mininet_wifi
from mn_wifi.sumo.runner import sumo
from mn_wifi.link import wmediumd, ITSLink
from mn_wifi.wmediumdConnector import interference
import paho.mqtt.publish as publish
import time


def publish_msg(user,message):
    MQTT_SERVER="127.0.0.1"
    MQTT_PATH="test-message-mqtt"
    publish.single(MQTT_PATH,message,hostname=MQTT_SERVER)
    
    
    	
def topology():

    "Create a network."
    net = Mininet_wifi(link=wmediumd, wmediumd_mode=interference)

    info("*** Creating nodes\n")
    for id in range(0, 20):
        net.addCar('car%s' % (id+1), wlans=2, encrypt=['wpa2', ''])

    kwargs = {'ssid': 'vanet-ssid', 'mode': 'g', 'passwd': '123456789a',
              'encrypt': 'wpa2', 'failMode': 'standalone', 'datapath': 'user'}
    e1 = net.addAccessPoint('e1', mac='00:00:00:11:00:01', channel='1',
                            position='2600,3500,0', **kwargs)
    e2 = net.addAccessPoint('e2', mac='00:00:00:11:00:02', channel='6',
                            position='2800,3500,0', **kwargs)
    e3 = net.addAccessPoint('e3', mac='00:00:00:11:00:03', channel='11',
                            position='3000,3500,0', **kwargs)
    e4 = net.addAccessPoint('e4', mac='00:00:00:11:00:04', channel='1',
                            position='2600,3300,0', **kwargs)
    e5 = net.addAccessPoint('e5', mac='00:00:00:11:00:05', channel='6',
                            position='2800,3300,0', **kwargs)
    e6 = net.addAccessPoint('e6', mac='00:00:00:11:00:06', channel='11',
                            position='3000,3300,0', **kwargs)

    info("*** Configuring Propagation Model\n")
    net.setPropagationModel(model="logDistance", exp=2.8)

    info("*** Configuring wifi nodes\n")
    net.configureWifiNodes()

    net.addLink(e1, e2)
    net.addLink(e2, e3)
    net.addLink(e3, e4)
    net.addLink(e4, e5)
    net.addLink(e5, e6)
    for car in net.cars:
        net.addLink(car, intf=car.wintfs[1].name,
                    cls=ITSLink, band=20, channel=181)

    net.useExternalProgram(program=sumo, port=8813,
                           config_file='map.sumocfg',
                           extra_params=["--start"])

    info("*** Starting network\n")
    net.build()

    for enb in net.aps:
        enb.start([])

    for id, car in enumerate(net.cars):
        car.setIP('192.168.0.%s/24' % (id+1), intf='%s-wlan0' % car.name)
        car.setIP('192.168.1.%s/24' % (id+1), intf='%s-wlan1' % car.name)
                
    i = 0
    while True:
        i+=1
        if i == 5000000:
            for car in enumerate(net.cars):
                 time.sleep(1)  
                 publish_msg(car[0],car[0])
            i=0

    info("*** Running CLI\n")
    CLI(net)

    info("*** Stopping network\n")
    net.stop()


if __name__ == '__main__':
    setLogLevel('info')

    os.system('mn -c')
    topology()
