#! /usr/bin/python3

from global_mapping import packet_types, flag_types
from packet import create_packet
from message import send_ACK

def normal(sessions, source, payload):
    
    sessions.add(source, payload)


def first_packet(sessions, source, payload):
   
    sessions.add(source, payload)


def last_packet(sock, sessions, source, sequance_number, payload):
    
    sessions.add(source, payload)

    send_ACK(sock, source, sequence_number)


def single_packet(sock, source, sequence_number, payload):
   
    print("Single packet, sending ACK...")
    # TODO sequance_number

    send_ACK(sock, source, sequence_number)


def ACK(user_messages, source, sequance_number):
    
    print('Received ACK from', source)
    user_messages.remove(source, sequance_number)


def NOT_ACK():
    pass
    # Send ACK


def error():
    pass
    # do something


def handle_flag(sock, sessions, user_messages, header, payload):
    
    flag = header.flag

    if flag == flag_types['normal']:
        normal(sessions, header.source, payload)
        return

    if flag == flag_types['first_packet']:
        first_packet(sessions, header.source, payload)
        return

    if flag == flag_types['last_packet']:
        last_packet(sock, sessions, header.source, header.sequance_number, payload)
        return

    if flag == flag_types['single_packet']:
        single_packet(sock, header.source, header.sequence_number, payload)
        return

    if flag == flag_types['ACK']:
        ACK(user_messages, header.source, header.sequance_number)
        return

    if flag == flag_types['NOT_ACK']:
        NOT_ACK()
        return

    if flag == flag_types['error']:
        error()
        return

