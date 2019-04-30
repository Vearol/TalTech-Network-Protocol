#! /usr/bin/python3

import socket
from threading import Thread

from header_parser import Header_Parser
from packet_handler import handle_packet
from flag_handler import handle_flag
from forward import forward_message
from sessions import UserSessions
from message import UserMessageACK, UserMessageSN, send_message, send_file
from nodes import Nodes
from global_mapping import packet_types, DEFAULT_DESTINATION, DEFAULT_SERVER_GPG


DEFAULT_SERVER_IP = '0.0.0.0'
DEFAULT_SERVER_PORT = 8080
DEFAULT_SERVER_GPG = 9223372036854775807


def listen(sock, parser, sessions, messages_ack, sequences, nodes):
    
    while True:
        # Receive bytes. 100 bytes in theory, can decrease later
        message_bytes, address_from = sock.recvfrom(2048)

        if (len(message_bytes) < 20):
            print('Input message size was less than 20 bytes. Invalid packet.')
            continue

        # Header takes first 20 bytes. Try to parse
        header = message_bytes[0:20]

        try:
            parser.parse_header(header)

        except IndexError:
            print('Couldn\'t parse header, skip packet')
            continue

        # Forward message
        if (parser.destination != DEFAULT_SERVER_GPG):
            forward_message(sock, message_bytes, parser.destination)
            continue

        # Payload - next 80 bytes(rest of bytes)
        payload = message_bytes[20:]        

        handle_flag(sock, sessions, sequences, messages_ack, parser, payload)
        handle_packet(sock, nodes, sessions, sequences, messages_ack, parser, payload)


def handle_input(sock, parser, sessions, messages_ack, sequences, nodes):

    while True:
        message = input('Enter message, of "file" if send file: ')
    
        if (message == 'file'):
            file_path = input('Enter file path: ')
            send_file(sock, sessions, sequences, messages_ack, packet_types['metadata_message'], DEFAULT_DESTINATION, file_path)
            continue
    
        send_message(sock, sessions, sequences, messages_ack, packet_types['screen_message'], DEFAULT_DESTINATION, message.encode())


sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((DEFAULT_SERVER_IP, DEFAULT_SERVER_PORT))
print('Listening socket:',DEFAULT_SERVER_IP, ':', DEFAULT_SERVER_PORT)

parser = Header_Parser()
sessions = UserSessions()
messages_ack = UserMessageACK()
sequences = UserMessageSN()
nodes = Nodes()

listen_thread = Thread(target=listen, args=(sock, parser, sessions, messages_ack, sequences, nodes))
listen_thread.start()

input_thread = Thread(target=handle_input, args=(sock, parser, sessions, messages_ack, sequences, nodes))
input_thread.start()
