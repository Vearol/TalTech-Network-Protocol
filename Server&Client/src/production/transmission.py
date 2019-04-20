#! /usr/bin/python3


import socket


TRANSMISSION_PORT = 1234


class Transmission:

    @staticmethod
    def broadcast_update_request(sock):
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        sock.bind("", TRANSMISSION_PORT)
        # sock.sendto()

    @staticmethod
    def forward_packet(sock, message, dest_ip, dest_port):
        print("Forwarding massage to {}:{}".format(dest_ip, dest_port))
        sock.sendto(message, (dest_ip, dest_port))
