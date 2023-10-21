# Lab3 Skeleton
#
# Hints/Reminders from Lab 3:
#
# To check the source and destination of an IP packet, you can use
# the header information... For example:

# To send an OpenFlow Message telling a switch to send packets out a
# port, do the following, replacing <PORT> with the port number the 
# switch should send the packets out:
#
#    msg = of.ofp_flow_mod()
#    msg.match = of.ofp_match.from_packet(packet)

#    msg.actions.append(of.ofp_action_output(port = <PORT>))
#    msg.data = packet_in
#    self.connection.send(msg)
#
# To drop packets, simply omit the action.
#

from pox.core import core
#from ipaddr import IPNetwork, IPAddress

import pox.openflow.libopenflow_01 as of

log = core.getLogger()

class Routing (object):
  """
  A Firewall object is created for each switch that connects.
  A Connection object for that switch is passed to the __init__ function.
  """
  def __init__ (self, connection):
    # Keep track of the connection to the switch so that we can
    # send it messages!
    self.connection = connection

    # This binds our PacketIn event listener
    connection.addListeners(self)

  def do_routing (self, packet, packet_in, port_on_switch, switch_id):
    # port_on_swtich - the port on which this packet was received
    # switch_id - the switch which received this packet

    # Your code here
    tcp = packet.find("tcp")
    icmp = packet.find("icmp")
    udp = packet.find("udp")

    sales_subnet = {'Laptop1': '10.0.0.10', 'Printer': '10.0.0.9', 'Laptop2': '10.0.0.8'}
    ot_subnet = {'Workstation1': '10.0.3.7', 'Workstation2': '10.0.3.6'}
    it_subnet = {'Workstation3': '10.0.2.5', 'Workstation4': '10.0.2.4'}
    data_subnet = {'Server2': '10.0.1.1', 'WebServer': '10.0.1.2', 'DNSserver': '10.0.1.3'}

    
    if icmp:
      ipv4 = packet.find("ipv4")
      if switch_id == 5:
        print("SWITCH 5")
        print(ipv4.srcip)
        print(ipv4.dstip)
        if ipv4.srcip in sales_subnet.values() and ipv4.dstip in ot_subnet.values():
          port = 2
          print("going to switch 2")
          self.accept(packet, packet_in, port)
        if ipv4.srcip in sales_subnet.values() and ipv4.dstip in it_subnet.values():
          port = 3
          print("going to switch 3")
          self.accept(packet, packet_in, port)
        if ipv4.srcip in ot_subnet.values() and ipv4.dstip in sales_subnet.values():
          port = 1
          print("going to switch 1")
          self.accept(packet, packet_in, port)
        if ipv4.srcip in ot_subnet.values() and ipv4.dstip in it_subnet.values():
          port = 3
          print("going to switch 3")
          self.accept(packet, packet_in, port)
        if ipv4.srcip in it_subnet.values() and ipv4.dstip in sales_subnet.values():
          port = 1
          print("going to switch 1")
          self.accept(packet, packet_in, port)
        if ipv4.srcip in it_subnet.values() and ipv4.dstip in ot_subnet.values():
          port = 2
          print("going to switch 2")
          self.accept(packet, packet_in, port)
      
      #sales Switch
      if switch_id == 1:
        print("Switch 1")
        #Within the Sales Department
        if ipv4.dstip in sales_subnet.values():
          print("ipv4 in Sales")
          if ipv4.dstip == '10.0.0.10':
            print("ipv4 == 10.0.0.10")
            port = 1
            self.accept(packet, packet_in, port)
          if ipv4.dstip == '10.0.0.9':
            print("ipv4 == 10.0.0.9")
            port = 2
            self.accept(packet, packet_in, port)
          if ipv4.dstip == '10.0.0.8':
            print("ipv4 == 10.0.0.8")
            port = 3
            self.accept(packet, packet_in, port)
        #to the OT Department or IT Department
        if ipv4.dstip in ot_subnet.values() or ipv4.dstip in it_subnet.values():
          port = 5
          self.accept(packet, packet_in, port)
        
      if switch_id == 3:
        print("Switch 3")
        #within the IT Department
        if ipv4.dstip in it_subnet.values():
          if ipv4.dstip == '10.0.2.5':
            port = 2
            self.accept(packet, packet_in, port)
          if ipv4.dstip == '10.0.2.4':
            port = 1
            self.accept(packet, packet_in, port)
        #to the sales Department or OT Department
        if ipv4.dstip in sales_subnet.values() or ipv4.dstip in ot_subnet.values():
          port = 7
          self.accept(packet, packet_in, port)

      if switch_id == 2:
        print("Switch 2")
        #within the OT department
        if ipv4.dstip in ot_subnet.values():
          print("ipv4 in OT")
          if ipv4.dstip == '10.0.3.6':
            print("ipv4=10.0.3.6")
            port = 2
            self.accept(packet, packet_in, port)
          if ipv4.dstip == '10.0.3.7':
            port = 1
            print("ipv4=10.0.3.7")
            self.accept(packet, packet_in, port)
        if ipv4.dstip in it_subnet.values() or ipv4.dstip in sales_subnet.values():
          port = 6
          self.accept(packet, packet_in, port)

    if tcp:
      ipv4 = packet.find("ipv4")
      if switch_id == 5:
        print("SWITCH 5")
        print(ipv4.srcip)
        print(ipv4.dstip)
        if ipv4.srcip in data_subnet.values() and ipv4.dstip in ot_subnet.values():
          port = 2
          print("going to switch 2")
          self.accept(packet, packet_in, port)
        if ipv4.srcip in data_subnet.values() and ipv4.dstip in it_subnet.values():
          port = 3
          print("going to switch 3")
          self.accept(packet, packet_in, port)
        if ipv4.srcip in ot_subnet.values() and ipv4.dstip in data_subnet.values():
          port = 4
          print("going to switch 4")
          self.accept(packet, packet_in, port)
        if ipv4.srcip in ot_subnet.values() and ipv4.dstip in it_subnet.values():
          port = 3
          print("going to switch 3")
          self.accept(packet, packet_in, port)
        if ipv4.srcip in it_subnet.values() and ipv4.dstip in data_subnet.values():
          port = 4
          print("going to switch 4")
          self.accept(packet, packet_in, port)
        if ipv4.srcip in it_subnet.values() and ipv4.dstip in ot_subnet.values():
          port = 2
          print("going to switch 2")
          self.accept(packet, packet_in, port)
      
      #Data Switch
      if switch_id == 4:
        print("Switch 4")
        #Within the Data Department
        if ipv4.dstip in data_subnet.values():
          print("ipv4 in data")
          if ipv4.dstip == '10.0.1.1':
            print("ipv4 == 10.0.1.1")
            port = 1
            self.accept(packet, packet_in, port)
          if ipv4.dstip == '10.0.1.2':
            print("ipv4 == 10.0.1.2")
            port = 2
            self.accept(packet, packet_in, port)
          if ipv4.dstip == '10.0.1.3':
            print("ipv4 == 10.0.1.3")
            port = 3
            self.accept(packet, packet_in, port)
        #to the OT Department or IT Department
        if ipv4.dstip in ot_subnet.values() or ipv4.dstip in it_subnet.values():
          port = 8
          self.accept(packet, packet_in, port)
        
      if switch_id == 3:
        print("Switch 3")
        #within the IT Department
        if ipv4.dstip in it_subnet.values():
          if ipv4.dstip == '10.0.2.5':
            port = 2
            self.accept(packet, packet_in, port)
          if ipv4.dstip == '10.0.2.4':
            port = 1
            self.accept(packet, packet_in, port)
        #to the sales Department or OT Department
        if ipv4.dstip in data_subnet.values() or ipv4.dstip in ot_subnet.values():
          port = 7
          self.accept(packet, packet_in, port)

      if switch_id == 2:
        print("Switch 2")
        #within the OT department
        if ipv4.dstip in ot_subnet.values():
          print("ipv4 in OT")
          if ipv4.dstip == '10.0.3.6':
            print("ipv4=10.0.3.6")
            port = 2
            self.accept(packet, packet_in, port)
          if ipv4.dstip == '10.0.3.7':
            port = 1
            print("ipv4=10.0.3.7")
            self.accept(packet, packet_in, port)
        if ipv4.dstip in it_subnet.values() or ipv4.dstip in data_subnet.values():
          port = 6
          self.accept(packet, packet_in, port)

    if udp:
      ipv4 = packet.find("ipv4")
      if switch_id == 5:
        print("SWITCH 5")
        print(ipv4.srcip)
        print(ipv4.dstip)
        if ipv4.srcip in sales_subnet.values() and ipv4.dstip in data_subnet.values():
          port = 4
          print("going to switch 4")
          self.accept(packet, packet_in, port)
        if ipv4.srcip in data_subnet.values() and ipv4.dstip in sales_subnet.values():
          port = 1
          print("going to switch 1")
          self.accept(packet, packet_in, port)
        if ipv4.srcip in sales_subnet.values() and ipv4.dstip in sales_subnet.values():
          port = 1
          print("going to switch 1")
          self.accept(packet, packet_in, port)
        if ipv4.srcip in data_subnet.values() and ipv4.dstip in data_subnet.values():
          port = 4
          print("going to switch 4")
          self.accept(packet, packet_in, port)
          
          
      if switch_id == 4:
        print("Switch 4")
        #Within the Data Department
        if ipv4.dstip in data_subnet.values():
          print("ipv4 in data")
          if ipv4.dstip == '10.0.1.1':
            print("ipv4 == 10.0.1.1")
            port = 1
            self.accept(packet, packet_in, port)
          if ipv4.dstip == '10.0.1.2':
            print("ipv4 == 10.0.1.2")
            port = 2
            self.accept(packet, packet_in, port)
          if ipv4.dstip == '10.0.1.3':
            print("ipv4 == 10.0.1.3")
            port = 3
            self.accept(packet, packet_in, port)
        #to the OT Department or IT Department
        if ipv4.dstip in sales_subnet.values():
          port = 8
          self.accept(packet, packet_in, port)

      if switch_id == 1:
        print("Switch 1")
        #Within the Data Department
        if ipv4.dstip in sales_subnet.values():
          print("ipv4 in data")
          if ipv4.dstip == '10.0.0.10':
            print("ipv4 == 10.0.0.10")
            port = 1
            self.accept(packet, packet_in, port)
          if ipv4.dstip == '10.0.0.9':
            print("ipv4 == 10.0.0.9")
            port = 2
            self.accept(packet, packet_in, port)
          if ipv4.dstip == '10.0.0.8':
            print("ipv4 == 10.0.0.8")
            port = 3
            self.accept(packet, packet_in, port)
        #to the OT Department or IT Department
        if ipv4.dstip in data_subnet.values():
          port = 5
          self.accept(packet, packet_in, port)

  
  def accept (self, packet, packet_in, portkp):

    msg = of.ofp_flow_mod()
    msg.match = of.ofp_match.from_packet(packet)
    msg.actions.append(of.ofp_action_output(port = portkp))
    msg.data = packet_in
    self.connection.send(msg)

  def drop (self, packet):

    msg = of.ofp_flow_mod()
    msg.match = of.ofp_match.from_packet(packet)
    msg.idle_timeout = 30
    msg.hard_timeout = 30
    self.connection.send(msg)


  def _handle_PacketIn (self, event):
    """
    Handles packet in messages from the switch.
    """
    packet = event.parsed # This is the parsed packet data.
    if not packet.parsed:
      log.warning("Ignoring incomplete packet")
      return

    packet_in = event.ofp # The actual ofp_packet_in message.
    self.do_routing(packet, packet_in, event.port, event.dpid)

def launch ():
  """
  Starts the component
  """
  def start_switch (event):
    log.debug("Controlling %s" % (event.connection,))
    Routing(event.connection)
  core.openflow.addListenerByName("ConnectionUp", start_switch)
