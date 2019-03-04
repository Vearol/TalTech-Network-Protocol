#! /usr/bin/python3

import socket

port = 8080

with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
    s.bind(('127.0.0.1', port))
    print('Listening socket: 127.0.0.1:', port)

    while True:
        message, address = s.recvfrom(10240)
        print("Message recieved: ", message.decode('utf-8'))