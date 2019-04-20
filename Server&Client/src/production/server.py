#! /usr/bin/python3

from header_parser import Header_Parser
from packet_handler import handle_packet
from flag_handler import handle_flag
from transmission import Transmission
from sessions import UserSessions
from message import UserMessageACK
import constants as c
import socket
import sys
sys.path.append("./")


with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
    sock.bind(('127.0.0.1', c.CONFIG['server_port']))
    print('Listening socket: 127.0.0.1:', c.CONFIG['server_port'])

    parser = Header_Parser()
    sessions = UserSessions()
    messages_ack = UserMessageACK()

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
        if (parser.destination != c.CONFIG['server_gpg']):
            Transmission.forward_packet(sock, message_bytes, parser.destination)
            continue

        # Payload - next 80 bytes(rest of bytes)
        payload = message_bytes[20:]

        handle_flag(sock, sessions, messages_ack, parser, payload)
        handle_packet(sock, parser, payload)
