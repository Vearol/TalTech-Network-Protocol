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

    @staticmethod
    def send_keepalive(sock, message, dest_ip, dest_port):
        print("send keepalive")

    @staticmethod
    def notify_route_update(sock, message, dest_ip, dest_port):
        print("route_update_message")

    @staticmethod
    def request_full_table(sock, message, dest_ip, dest_port):
        print("send full table request")

    @staticmethod
    def send_full_table(sock, message, dest_ip, dest_port):
        print("send full table data")

    @staticmethod
    def send_screen_message(sock, message, dest_ip, dest_port):
        message_str = message.decode('utf-8')
        print("message for screen from")

    @staticmethod
    def send_metadata(sock, message, dest_ip, dest_port):
        print("message with binary metadata")

    @staticmethod
    def request_identity(sock, message, dest_ip, dest_port):
        print("request identity")

    @staticmethod
    def send_identity():
        print("send identity")
