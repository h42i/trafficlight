import usnmp
import time
import socket
import sys
import gc

def main():
    agent_ip = "10.23.42.254"
    agent_port = 161
    agent_community = "public"
    # oid of input on wan-port
    oid_if_inoct = "1.3.6.1.2.1.2.2.1.10.9"
    #inter-poll delay, in seconds
    delay = 1
    # oid of uptime
    oid_uptime = "1.3.6.1.2.1.1.3.0"
    oid_speed = "1.3.6.1.2.1.2.2.1.5.9"

    gc.collect()

    s = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
    s.settimeout(1)

    greq = usnmp.SnmpPacket(type=usnmp.SNMP_GETREQUEST, community=agent_community, id=time.ticks_us())
    for i in (oid_speed, oid_uptime, oid_if_inoct):
        greq.varbinds[i] = None

    s.sendto(greq.tobytes(), (agent_ip, agent_port))
    d = s.recvfrom(1024)
    gresp = usnmp.SnmpPacket(d[0])

    last_ut = gresp.varbinds[oid_uptime][1]
    last_in8 = gresp.varbinds[oid_if_inoct][1]

    while True:
        gc.collect()

        speed = gresp.varbinds[oid_speed][1]

        time.sleep(delay)

        greq.id=time.ticks_us()
        s.sendto(greq.tobytes(), (agent_ip, agent_port))
        try:
            d = s.recvfrom(1024)

            gresp = usnmp.SnmpPacket(d[0])

            if greq.id == gresp.id:
                ut = gresp.varbinds[oid_uptime][1]
                in8 = gresp.varbinds[oid_if_inoct][1]

                if in8 != last_in8:
                    print("new traffic value.")

                    timediff = ut - last_ut
                    traffic = in8 - last_in8

                    mbps = (traffic * 8 * 100) / (timediff/100 * speed)

                    print("  -->  " + str(timediff/100) + " seconds")
                    print("  -->  " + str(mbps) + " Mb/s")

                    last_in8 = in8
                    last_ut = ut

        except Exception as e:
            print("error")
            print(e.args[0])
