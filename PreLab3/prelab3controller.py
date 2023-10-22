# preLab3 controller Skeleton
#
# Based on of_tutorial by James McCauley

from pox.core import core
import pox.openflow.libopenflow_01 as of
import pox.lib.packet as pkt
import time
from pox.lib.addresses import IPAddr
from pox.lib.packet.ethernet import ethernet
from pox.lib.packet.ipv4 import ipv4
from pox.lib.packet.icmp import icmp
from pox.lib.packet.dns import dns

log = core.getLogger()

class Firewall (object):
  """
  A Firewall object is created for each switch that connects.
  A Connection object for that switch is passed to the __init__ function.
  """
  def __init__ (self, connection):
    # Keep track of the connection to the switch so that we can
    # send it messages!
    self.connection = connection
    self.check = time.time()

    # This binds our PacketIn event listener
    connection.addListeners(self)

  def do_firewall (self, packet, packet_in):
    # The code in here will be executed for every packet.

    arp = packet.find("arp")
    tcp = packet.find("tcp")
    icmp = packet.find("icmp")
    ipv4 = packet.find("ipv4")
    udp = packet.find("udp")
      
    if arp is not None or udp is not None:
      self.accept(packet, packet_in)

    if icmp is not None:
      if ipv4.srcip == '10.0.0.3' or ipv4.dstip == '10.0.0.3':
        self.drop(packet, packet_in)   
      if ipv4 is not None:
        self.accept(packet, packet_in)

    if tcp is not None and ipv4 is not None:
      if (ipv4.srcip == '10.0.0.6' and ipv4.dstip == '10.0.0.7') or (ipv4.srcip == '10.0.0.7' and ipv4.dstip == '10.0.0.6'):
        self.accept(packet, packet_in)
      elif (ipv4.srcip == '10.0.0.4' and ipv4.dstip == '10.0.0.10') or (ipv4.srcip == '10.0.0.10' and ipv4.dstip == '10.0.0.4'):
        self.accept(packet, packet_in)
      elif (ipv4.srcip == '10.0.0.6' and ipv4.dstip == '10.0.0.1') or (ipv4.srcip == '10.0.0.1' and ipv4.dstip == '10.0.0.6'):
        self.accept(packet, packet_in)
      elif (ipv4.srcip == '10.0.0.11' and ipv4.dstip == '10.0.0.2') or (ipv4.srcip == '10.0.0.2' and ipv4.dstip == '10.0.0.11'):
        self.accept(packet, packet_in)
      elif (ipv4.srcip == '10.0.0.10' and ipv4.dstip == '10.0.0.9') or (ipv4.srcip == '10.0.0.9' and ipv4.dstip == '10.0.0.10'):
        self.accept(packet, packet_in)
      elif (ipv4.srcip == '10.0.0.8' and ipv4.dstip == '10.0.0.9') or (ipv4.srcip == '10.0.0.9' and ipv4.dstip == '10.0.0.8'):
        self.accept(packet, packet_in)
      else:
        self.drop(packet, packet_in)
    else:
      self.drop(packet, packet_in)
  
  def accept (self, packet, packet_in):

    msg = of.ofp_flow_mod()
    msg.match = of.ofp_match.from_packet(packet)
    msg.idle_timeout = 30
    msg.hard_timeout = 30
    msg.actions.append(of.ofp_action_output(port = of.OFPP_FLOOD))
    msg.data = packet_in
    self.connection.send(msg)

  def drop (self, packet, packet_in):

    msg = of.ofp_flow_mod()
    msg.match = of.ofp_match.from_packet(packet)
    msg.idle_timeout = 30
    msg.hard_timeout = 30
    msg.buffer_id = packet_in.buffer_id
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
    self.do_firewall(packet, packet_in)

def launch ():
  """
  Starts the component
  """
  def start_switch (event):
    log.debug("Controlling %s" % (event.connection,))
    Firewall(event.connection)
  core.openflow.addListenerByName("ConnectionUp", start_switch)
