#! /usr/bin/python3

import socket

port = 8080

with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:

    while True:
        message = input('Enter message ')
        s.sendto(bytes(message, 'utf-8'), ('127.0.0.1', port))

