#! /usr/bin/python3

import socket

port = 8088

with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
    s.bind(('127.0.0.1', port))
    print('Listening socket: 127.0.0.1:', port)

    while True:
        message_bytes, address_from = s.recvfrom(10240)

        message_str = message_bytes.decode('utf-8')
    
        message_params = message_str.split('|')
        message_text = message_params[0]
        
        print("Message recieved:", message_text)