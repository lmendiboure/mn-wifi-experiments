#!/usr/bin/python

"""Example with a core infra: network switches and controller

Archi considered here:


C1 - controller - connected to both AP - Access Points - and S - Switches 

H1 could be seen as a potentiel server or broker located within the network
  

 AP1 ----            ----AP4
	/          /
 AP2 -- S1 <- S3 -> S2 -- AP5
      /      /     /
 AP3--      H1     ----- AP6
	  

***Requirements***:

Kernel version: 5.8+ (due to the 802.11p support)
sumo 1.5.0 or higher
sumo-gui"""

import os
from mininet.node import Controller, OVSKernelSwitch, RemoteController
from mn_wifi.node import UserAP
from mininet.log import setLogLevel, info
from mn_wifi.cli import CLI
from mn_wifi.net import Mininet_wifi
from mn_wifi.sumo.runner import sumo
from mn_wifi.link import wmediumd, ITSLink
from mn_wifi.wmediumdConnector import interference
import time

    
    
    	
def topology():

    "Create a network."
    net = Mininet_wifi(controller=Controller,accessPoint=UserAP, switch=OVSKernelSwitch, link=wmediumd, wmediumd_mode=interference)

    info("*** Creating nodes - Cars + Controller + Switches + Access Points + Host \n")
    for id in range(0, 20):
        net.addCar('car%s' % (id+1), wlans=2, encrypt=['wpa2', ''])

    c1 = net.addController('c1')
    s1 = net.addSwitch('s1')
    s2 = net.addSwitch('s2')
    s3 = net.addSwitch('s3')
    h1 = net.addHost('h1')

    kwargs = {'ssid': 'vanet-ssid', 'mode': 'g', 'passwd': '123456789a',
              'encrypt': 'wpa2', 'failMode': 'standalone', 'datapath': 'user'}
    
    
    ap1 = net.addAccessPoint('e1', mac='00:00:00:11:00:01', channel='1',
                            position='2600,3500,0', **kwargs)
    ap2 = net.addAccessPoint('e2', mac='00:00:00:11:00:02', channel='6',
                            position='2800,3500,0', **kwargs)
    ap3 = net.addAccessPoint('e3', mac='00:00:00:11:00:03', channel='11',
                            position='3000,3500,0', **kwargs)
    ap4 = net.addAccessPoint('e4', mac='00:00:00:11:00:04', channel='1',
                            position='2600,3300,0', **kwargs)
    ap5 = net.addAccessPoint('e5', mac='00:00:00:11:00:05', channel='6',
                            position='2800,3300,0', **kwargs)
    ap6 = net.addAccessPoint('e6', mac='00:00:00:11:00:06', channel='11',
                            position='3000,3300,0', **kwargs)

    info("*** Configuring Propagation Model\n")
    net.setPropagationModel(model="logDistance", exp=2.8)

    info("*** Configuring wifi nodes\n")
    net.configureWifiNodes()
    net.addLink(s1, s3)
    net.addLink(s2, s3)
    net.addLink(s3, h1)
    net.addLink(s1, ap1)
    net.addLink(s1, ap2)
    net.addLink(s2, ap3)
    net.addLink(s2, ap4)
    net.addLink(s2, ap5)
    net.addLink(s2, ap6)
 
    for car in net.cars:
        net.addLink(car, intf=car.wintfs[1].name,
                    cls=ITSLink, band=20, channel=181)

    net.useExternalProgram(program=sumo, port=8813,
                           config_file='map.sumocfg',
                           extra_params=["--start"])

    info("*** Starting network\n")
    net.build()
    
    c1.start()

    for enb in net.aps:
        enb.start([c1])
        
        

    for id, car in enumerate(net.cars):
        car.setIP('192.168.0.%s/24' % (id+1), intf='%s-wlan0' % car.name)
        car.setIP('192.168.1.%s/24' % (id+1), intf='%s-wlan1' % car.name)

    CLI(net)

    info("*** Stopping network\n")
    net.stop()


if __name__ == '__main__':
    setLogLevel('info')

    os.system('mn -c')
    topology()
