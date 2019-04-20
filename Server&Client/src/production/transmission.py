#! /usr/bin/python3


import socket
import constants as c


class Transmission:

    @staticmethod
    def broadcast_update_request():
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
            sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
            sock.bind("", c.CONFIG['transmission_port'])
            # sock.sendto()

    @staticmethod
    def forward_packet(sock, message, dest_ip, dest_port):
        print("Forwarding massage to {}:{}".format(dest_ip, dest_port))
        sock.sendto(message, (dest_ip, dest_port))
