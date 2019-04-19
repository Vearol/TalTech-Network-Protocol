#! /usr/bin/python3

from global_mapping import packet_types, flag_types
from packet import create_packet

def normal(sessions, user_id, payload):
    
    sessions.add(user_id, payload)


def first_packet(sessions, user_id, payload):
   
    sessions.add(user_id, payload)


def last_packet(sock, sessions, user_id, payload):
    
    sessions.add(user_id, payload)

    # TODO craft file, or whatever comes
    print(sessions.user_data[user_id])

    print("Single packet, sending ACK...")
    # TODO sequance_number
    packet = create_packet(PROTOCOL_VERSION, packet_types['metadata_message'], flag_types['ACK'], SERVER_KEY, user_id, 0, 0, bytes(0))

    destination = get_next_dest(user_id)
    sock.sendto(packet, (destination.ip, destination.port))


def single_packet(sock, user_id, payload):
   
    print("Single packet, sending ACK...")
    # TODO sequance_number
    packet = create_packet(PROTOCOL_VERSION, packet_types['metadata_message'], flag_types['ACK'], SERVER_KEY, user_id, 0, 0, bytes(0))

    destination = get_next_dest(user_id)
    sock.sendto(packet, (destination.ip, destination.port))


def ACK(user_messages, user_id, sequance_number):
    
    user_messages.remove(user_id, sequance_number)


def NOT_ACK():

    # Send ACK


def error():
    
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
        last_packet(sock, sessions, header.source, payload)
        return

    if flag == flag_types['single_packet']:
        single_packet(sock, sessions, header.source, payload)
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

