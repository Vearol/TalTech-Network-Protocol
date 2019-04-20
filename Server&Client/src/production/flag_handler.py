#! /usr/bin/python3

import constants as c
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
    packet = create_packet(c.PROTOCOL_VERSION, c.PACKET_TYPE['metadata_message'], c.FLAG_TYPE['ACK'], c.SERVER_KEY, user_id, 0, 0, bytes(0))

    destination = get_next_dest(user_id)
    sock.sendto(packet, (destination.ip, destination.port))


def single_packet(sock, user_id, payload):
   
    print("Single packet, sending ACK...")
    # TODO sequance_number
    packet = create_packet(c.PROTOCOL_VERSION, c.PACKET_TYPE['metadata_message'], c.FLAG_TYPE['ACK'], c.CONFIG['server_key'], user_id, 0, 0, bytes(0))

    destination = get_next_dest(user_id)
    sock.sendto(packet, (destination.ip, destination.port))


def ACK(user_messages, user_id, sequance_number):
    
    user_messages.remove(user_id, sequance_number)


def NOT_ACK():
    pass
    # Send ACK


def error():
    pass
    # do something


def handle_flag(sock, sessions, user_messages, header, payload):
    
    flag = header.flag

    if flag == c.FLAG_TYPE['normal']:
        normal(sessions, header.source, payload)
        return

    if flag == c.FLAG_TYPE['first_packet']:
        first_packet(sessions, header.source, payload)
        return

    if flag == c.FLAG_TYPE['last_packet']:
        last_packet(sock, sessions, header.source, payload)
        return

    if flag == c.FLAG_TYPE['single_packet']:
        single_packet(sock, sessions, header.source, payload)
        return

    if flag == c.FLAG_TYPE['ACK']:
        ACK(user_messages, header.source, header.sequance_number)
        return

    if flag == c.FLAG_TYPE['NOT_ACK']:
        NOT_ACK()
        return

    if flag == c.FLAG_TYPE['error']:
        error()
        return

