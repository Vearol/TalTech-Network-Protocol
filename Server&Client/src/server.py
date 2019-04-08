#! /usr/bin/python3

import socket
import sys
sys.path.append("./") 

from header_parser import Header_Parser
from packet_type_handler import *

default_server_ip = '127.0.0.1'
default_server_port = 8080

with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
    s.bind(('127.0.0.1', default_server_port))
    print('Listening socket: 127.0.0.1:', default_server_port)

    while True:
        message_bytes, address_from = s.recvfrom(10240)

        header = message_bytes[0:20]
        message_payload = message_bytes[20:]

        parser = Header_Parser()

        try:
            parser.parse_header(header)
            
            handle_packet_type(parser.packet_type)
        except:
            print('Invalid header')
            # and do something




#s.sendto(bytes(message_text, 'utf-8'), (destination_ip, int(destination_port)))
#message_str = message_bytes.decode('utf-8')
