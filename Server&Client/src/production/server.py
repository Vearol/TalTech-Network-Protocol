#! /usr/bin/python3

import socket
from threading import Thread
import time

from header_parser import Header_Parser
from packet_handler import handle_packet
from flag_handler import handle_flag
from sessions import UserSessions
from message import UserMessageACK, Message
from sequences import UserMessageSN
from nodes import Nodes
from global_config import packet_types, SERVER_KEY, DEFAULT_SERVER_IP, DEFAULT_SERVER_PORT, HEADER_BUFFER
from colors import colors
from global_data import GlobalData


def listen():
    
    while True:
        # Receive bytes. 100 bytes in theory, can decrease later
        message_bytes, address_from = GlobalData.sock.recvfrom(100)

        if (len(message_bytes) < HEADER_BUFFER):
            print(colors.ERROR, 'Input message size was less than 20 bytes. Invalid packet.')
            continue

        # Header takes first 20 bytes. Try to parse
        header_bytes = message_bytes[0:HEADER_BUFFER]

        try:
            GlobalData.header.parse(header_bytes)

        except IndexError:
            print(colors.ERROR, 'Couldn\'t parse header, skip packet')
            continue

        # Forward message
        destination = GlobalData.header.destination
        if (destination.lower() != SERVER_KEY.lower()):
            Message.forward(message_bytes, destination)
            continue

        # Payload - next 80 bytes(rest of bytes)
        payload = message_bytes[HEADER_BUFFER:]       

        handle_flag(payload)
        handle_packet(payload)


def handle_input():

    MSG_PROMPT = colors.INPUT + 'Enter message, of "file" if send file: ' + colors.TEXT
    FILE_PROMPT = colors.INPUT + 'Enter file path: ' + colors.TEXT
    DEST_PROMPT = colors.INPUT + 'Enter destination id: ' + colors.TEXT

    while True:
        time.sleep(0.5)
        dest = input(DEST_PROMPT)
        message = input(MSG_PROMPT)

        if (message == 'file'):
            file_path = input(FILE_PROMPT)
            Message.send_file(dest, file_path)
            continue

        Message.send_message(packet_types['screen_message'], dest, message.encode())


sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((DEFAULT_SERVER_IP, DEFAULT_SERVER_PORT))
print(colors.SERVER, 'Listening socket:',DEFAULT_SERVER_IP, ':', DEFAULT_SERVER_PORT)

header_parser = Header_Parser()
sessions = UserSessions()
messages = UserMessageACK()
sequences = UserMessageSN()
nodes = Nodes()

GlobalData.set_data(sock, sequences, sessions, messages, nodes, header_parser)

listen_thread = Thread(target=listen)
listen_thread.start()

input_thread = Thread(target=handle_input)
input_thread.start()
