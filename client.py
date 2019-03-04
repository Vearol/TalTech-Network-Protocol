#! /usr/bin/python3

import socket

default_server_port = 8080

with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:

    while True:
        text_message = input('Enter message: ')

        destination_ip = input('Enter destination ip: ')
        destination_port = input('Enter destination port: ')

        try:
            destination_port_int = int(destination_port)
        
            message = text_message + '|' + destination_ip + ':' + destination_port

            s.sendto(bytes(message, 'utf-8'), (destination_ip, destination_port_int))

        except:
            s.sendto(bytes(text_message, 'utf-8'), ('127.0.0.1', default_server_port))

