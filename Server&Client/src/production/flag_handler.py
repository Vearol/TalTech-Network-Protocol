#! /usr/bin/python3

from global_mapping import packet_types, flag_types, METADATA_HEADER
from packet import create_packet
from message import send_ACK
from byte_parser import bytes_to_number


def skip_index(payload, packet_type):
    
    if (packet_type == packet_types['metadata_message']):
        return METADATA_HEADER + bytes_to_number(payload[0 : METADATA_HEADER])
    
    return 0


def normal(sessions, source, packet_type, payload):
    
    skip = skip_index(payload, packet_type)
    sessions.add(source, payload[skip:])


def first_packet(sessions, source, payload):
   
    sessions.add(source, payload)


def last_packet(sock, sessions, source, packet_type, sequence_number, payload):
    
    skip = skip_index(payload, packet_type)
    sessions.add(source, payload[skip:])

    send_ACK(sock, source, sequence_number)


def single_packet(sock, source, sequence_number, payload):
   
    print("Single packet, sending ACK...")
    # TODO sequence_number check

    send_ACK(sock, source, sequence_number)


def ACK(user_messages, source, sequence_number):
    
    print('Received ACK from', source)
    #user_messages.remove(source, sequence_number)


def NOT_ACK():
    pass
    # Send ACK


def error():
    pass
    # do something


def handle_flag(sock, sessions, user_messages, header, payload):
    
    flag = header.flag

    if flag == flag_types['normal']:
        normal(sessions, header.source, header.packet_type, payload)
        return

    if flag == flag_types['first_packet']:
        first_packet(sessions, header.source, payload)
        return

    if flag == flag_types['last_packet']:
        last_packet(sock, sessions, header.source, header.packet_type, header.sequence_number, payload)
        return

    if flag == flag_types['single_packet']:
        single_packet(sock, header.source, header.sequence_number, payload)
        return

    if flag == flag_types['ACK']:
        ACK(user_messages, header.source, header.sequence_number)
        return

    if flag == flag_types['NOT_ACK']:
        NOT_ACK()
        return

    if flag == flag_types['error']:
        error()
        return

