#! /usr/bin/python3

import socket

default_server_ip = '127.0.0.1'
default_server_port = 8080

with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
    s.bind(('127.0.0.1', default_server_port))
    print('Listening socket: 127.0.0.1:', default_server_port)

    while True:
        message_bytes, address_from = s.recvfrom(10240)

        message_str = message_bytes.decode('utf-8')
    
        message_params = message_str.split('|')
        message_text = message_params[0]
        
        print("Message recieved:", message_text)
        
        message_destination = "127.0.0.1:8080"

    try:
            message_destination = message_params[1]
            
            print("Message destination:", message_destination)            

    except:
            print('Message destination is invalid')

    try:
        destination_params = message_destination.split(':')

        destination_ip = destination_params[0]
        destination_port = destination_params[1]
            
        if (destination_ip == default_server_ip and destination_port == default_server_port):
            print('Message for this server')
        else:
            s.sendto(bytes(message_text, 'utf-8'), (destination_ip, int(destination_port)))
    except:
        print('Couldn\'t parse destination params')

    
    