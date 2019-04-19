#! /usr/bin/python3

from global_mapping import *

def keep_alive(payload):
    
    print('keep alive message')
    # do something


def route_update(payload):
   
    print('route update message')
    # do something


def full_table_request(payload):
    
    print('request full active routing table message')
    # do something


def full_table_update(payload):
   
    print('full table update message')
    # do something


def send_request_identity(payload):
    
    print('sent/request identity message')
    # do something


def screen_message(socket, header, payload):
    
    message_str = payload.decode('utf-8')

    source = header.source

    # TODO store in db
    print('message for screen from', source)
    print(message_str)

    # Send ACK


def metadata_message(payload):
    
    print('message with binary metadata')
    # do something


def handle_packet(socket, header, payload):
    
    packet_type = header.packet_type

    if packet_type == packet_types['keepalive']:
        keep_alive(payload)
        return

    if packet_type == packet_types['route_update']:
        route_update(payload)
        return

    if packet_type == packet_types['full_table_request']:
        full_table_request(payload)
        return

    if packet_type == packet_types['full_table_update']:
        full_table_update(payload)
        return

    if packet_type == packet_types['send_request_identity']:
        send_request_identity(payload)
        return

    if packet_type == packet_types['screen_message']:
        screen_message(socket, header, payload)
        return

    if packet_type == packet_types['metadata_message']:
        metadata_message(payload)
        return

