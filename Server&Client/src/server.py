#! /usr/bin/python3

import socket
import sys
sys.path.append("./") 

from header_parser import Header_Parser
from packet_type_handler import handle_packet
from flag_handler import handle_flag
from forward import forward_message
from sessions import UserSessions
from message import UserMeesageACK

default_server_ip = '127.0.0.1'
default_server_port = 8080
default_server_gpg = 9223372036854775807

with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
    sock.bind(('127.0.0.1', default_server_port))
    print('Listening socket: 127.0.0.1:', default_server_port)

    while True:
        # Receive bytes. 100 bytes in theory, can decrease later
        message_bytes, address_from = sock.recvfrom(2048)

        if (len(message_bytes) < 20):
            print('Input message size was less than 20 bytes. Invalid packet.')
            continue

        # Header takes first 20 bytes. Try to parse
        header = message_bytes[0:20]
        parser = Header_Parser()

        try:
            parser.parse_header(header)
            
        except:
            print('Couldn\'t parse header, skip packet')
            continue

        # Forward message
        if (parser.destination != default_server_gpg):
            forward_message(sock, message_bytes, parser.destination)
            continue
        
        # Payload - next 80 bytes(rest of bytes)
        payload = message_bytes[20:]

        user_sessions = UserSessions()
        user_messages = UserMeesageACK()

        handle_flag(sock user_sessions, user_messages, parser, payload)
        handle_packet(sock, parser, payload)
        


#s.sendto(bytes(message_text, 'utf-8'), (destination_ip, int(destination_port)))