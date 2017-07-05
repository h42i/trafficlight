import usnmp
import time
import socket
import sys
import gc

class Traffic:

    agent_ip = "10.23.42.254"
    agent_port = 161
    agent_community = "public"
    # oid of incoming bytes on wan-port
    oid_if_inoct = "1.3.6.1.2.1.2.2.1.10.9"
    # oid of uptime
    oid_uptime = "1.3.6.1.2.1.1.3.0"
    # oid of ports speed
    oid_speed = "1.3.6.1.2.1.2.2.1.5.9"

    sock = None
    greq = None
    gresp = None
    last_ut = None
    last_in8 = None
    speed = None

    def __init__(self):
        gc.collect()

        self.sock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
        self.sock.settimeout(1)

        self.greq = usnmp.SnmpPacket(type=usnmp.SNMP_GETREQUEST, community=self.agent_community, id=time.ticks_us())
        for i in (self.oid_speed, self.oid_uptime, self.oid_if_inoct):
            self.greq.varbinds[i] = None

        self.sock.sendto(self.greq.tobytes(), (self.agent_ip, self.agent_port))
        d = self.sock.recvfrom(1024)
        self.gresp = usnmp.SnmpPacket(d[0])

        self.last_ut = self.gresp.varbinds[self.oid_uptime][1]
        self.last_in8 = self.gresp.varbinds[self.oid_if_inoct][1]

    def get_traffic(self):
        gc.collect()

        speed = self.gresp.varbinds[self.oid_speed][1]

        time.sleep(1)

        self.greq.id = time.ticks_us()
        self.sock.sendto(self.greq.tobytes(), (self.agent_ip, self.agent_port))

        try:
            d = self.sock.recvfrom(1024)

            self.gresp = usnmp.SnmpPacket(d[0])

            if self.greq.id == self.gresp.id:
                ut = self.gresp.varbinds[self.oid_uptime][1]
                in8 = self.gresp.varbinds[self.oid_if_inoct][1]

                if in8 != self.last_in8:
                    print("New traffic value!")

                    timediff = ut - self.last_ut
                    traffic = in8 - self.last_in8

                    mbps = (traffic * 8 * 100) / (timediff/100 * speed)

                    print("  -->  " + str(timediff/100) + " seconds")
                    print("  -->  " + str(mbps) + " Mb/s")

                    self.last_in8 = in8
                    self.last_ut = ut

                    return mbps

        except Exception as e:
            print("error")
            print(e.args[0])
            return 0
