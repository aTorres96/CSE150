#!/usr/bin/python

from mininet.topo import Topo
from mininet.net import Mininet
from mininet.util import dumpNodeConnections
from mininet.log import setLogLevel
from mininet.cli import CLI
from mininet.node import RemoteController

class final_topo(Topo):
  def build(self):

    laptop1 = self.addHost('Laptop1',mac="00:00:00:00:00:10", ip='10.0.0.10/24',defaultRoute="Laptop1-eth1")
    printer = self.addHost('Printer',mac="00:00:00:00:00:09", ip='10.0.0.9/24',defaultRoute="Printer-eth1")
    laptop2 = self.addHost('Laptop2',mac="00:00:00:00:00:08", ip='10.0.0.8/24',defaultRoute="Laptop2-eth1")
    ws1 = self.addHost('ws1',mac="00:00:00:00:00:07", ip='10.0.3.7/24',defaultRoute="ws1-eth1")
    ws2 = self.addHost('ws2',mac="00:00:00:00:00:06", ip='10.0.3.6/24',defaultRoute="ws2-eth1")
    ws3 = self.addHost('ws3',mac="00:00:00:00:00:05", ip='10.0.2.5/24',defaultRoute="ws3-eth1")
    ws4 = self.addHost('ws4',mac="00:00:00:00:00:04", ip='10.0.2.4/24',defaultRoute="ws4-eth1")
    dnsServer = self.addHost('DNSserver',mac="00:00:00:00:00:03", ip='10.0.1.3/24',defaultRoute="DNSserver-eth1")
    webServer = self.addHost('WebServer',mac="00:00:00:00:00:02", ip='10.0.1.2/24',defaultRoute="WebServer-eth1")
    server2 = self.addHost('Server2',mac="00:00:00:00:00:01", ip='10.0.1.1/24',defaultRoute="Server2-eth1")

    coreSwitch = self.addSwitch('s5')
    switch1 = self.addSwitch('s1')
    switch2 = self.addSwitch('s2')
    switch3 = self.addSwitch('s3')
    switch4 = self.addSwitch('s4')

    self.addLink(coreSwitch, switch1, port1=1, port2=5)
    self.addLink(coreSwitch, switch2, port1=2, port2=6)
    self.addLink(coreSwitch, switch3, port1=3, port2=7)
    self.addLink(coreSwitch, switch4, port1=4, port2=8)



    self.addLink(laptop1, switch1, port1=1, port2=1)
    self.addLink(printer, switch1, port1=1, port2=2)
    self.addLink(laptop2, switch1, port1=1, port2=3)
    self.addLink(ws1, switch2, port1=1, port2=1)
    self.addLink(ws2, switch2, port1=1, port2=2)
    self.addLink(ws3, switch3, port1=1, port2=2)
    self.addLink(ws4, switch3, port1=1, port2=1)
    self.addLink(webServer, switch4, port1=1, port2=2)
    self.addLink(server2, switch4, port1=1, port2=1)
    self.addLink(dnsServer, switch4, port1=1, port2=3)

def configure():
  topo = final_topo()
  net = Mininet(topo=topo, controller=RemoteController)
  net.start()
  # use static ARP
  net.staticArp() 
  CLI(net)
  
  net.stop()


if __name__ == '__main__':
  configure()
