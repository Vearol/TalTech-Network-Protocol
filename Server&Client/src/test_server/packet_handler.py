#! /usr/bin/python3

import json

from global_config import packet_types, flag_types, FILENAME_KEY, FILESIZE_KEY, SERVER_KEY, ID_KEY, RESPONCE_KEY, NAME_KEY
from global_data import GlobalData
from message import Message
from byte_parser import bytes_to_number, bytes_to_GPG, number_to_bytes
from json_parser import parse_file_metadata, generate_identity_bytes
from colors import colors


def keep_alive(header):
    
    GlobalData.keepalives.update_user(header.source)


def route_update(header, payload):
    
    log = 'Route update from: ' + str(header.source)
    print(colors.LOG, log)

    if (GlobalData.nodes.is_updated(header.source, payload)):
        GlobalData.nodes.update_table(header.source, payload)
        
        updated_node = bytes_to_GPG(payload[0:8])
        updated_cost = bytes_to_number(payload[8:10])
        payload[8:10] = number_to_bytes(updated_cost + 1, 2)
        
        neighbors = GlobalData.nodes.get_neighbors()
        Message.send_message_to_group(packet_types['route_update'], neighbors, payload)

        if (GlobalData.nodes.get_nickname(updated_node) == ""):
            Message.send_identity_request(updated_node)


def full_table_request(destination):
    
    log = str(destination) + ' requested full routing table'
    print(colors.LOG, log)
    # TODO check data format
    payload = GlobalData.nodes.get_full_table_byte()

    Message.send_message(packet_types['full_table_update'], destination, payload)


def full_table_update(source, flag, payload):
    
    log = 'Full table update from: ' + str(source)
    print(colors.LOG, log)

    GlobalData.nodes.remove_table(source)

    if (flag == flag_types['single_packet']):
        GlobalData.nodes.add_table_byte(payload)
        return
    
    payload_data = GlobalData.sessions.get_data(source)

    GlobalData.nodes.add_table_byte(payload_data)

    new_nodes = GlobalData.nodes.get_unknown_nodes()
    for node in new_nodes:
        Message.send_identity_request(node)


def send_request_identity(header, payload):

    identity_data = json.load(payload.decode())

    GlobalData.nodes.set_nickname(header.source, identity_data[NAME_KEY])

    log = 'Received identity of ' + str(header.source) + ': ' + str(identity_data[NAME_KEY])
    print(colors.LOG, log)

    responce_required = bool(identity_data[RESPONCE_KEY])
    if (responce_required):

        server_identity = generate_identity_bytes('false')

        Message.send_message(header.packet_type, header.source, server_identity)


def group_message(header, payload):
    source = header.source

    print(colors.INCOME, 'group message from', source)

    if (header.flag == flag_types['single_packet']):
        
        message_str = payload.decode('utf-8')    
        print('>', colors.TEXT, message_str)
    else:
        print(colors.ERROR, 'Not supported multi-packet group messages')


def screen_message(header, payload):
    
    source = header.source

    print(colors.INCOME, 'message for screen from', source)

    if (header.flag == flag_types['single_packet']):
        
        message_str = payload.decode('utf-8')    
        print('>', colors.TEXT, message_str)
        return

    payload_data = GlobalData.sessions.get_data(source)

    message_str = payload_data.decode()
    # TODO store in db
    
    print('>', colors.TEXT, message_str)
    
    GlobalData.sessions.remove(source)


def metadata_message(header, payload):

    source = header.source
    
    payload_data = payload
    if (header.flag == flag_types['last_packet']):
        payload_data = GlobalData.sessions.get_data(source)

    print(colors.LOG, 'message with binary metadata from', header.source)

    metadata, skip = parse_file_metadata(payload_data)

    file_name = 'file_name'
    file_size = 0

    keys = metadata.keys()
    if (FILENAME_KEY in keys):
        file_name = metadata[FILENAME_KEY]
    if (FILESIZE_KEY in keys):
        file_size = metadata[FILESIZE_KEY]

    print(colors.INCOME, 'Saving file:', file_name, file_size, 'bytes')

    file_to_save = open(file_name, 'wb')
    

    file_data = payload_data[skip:]
    file_to_save.write(file_data)

    file_to_save.close()

    GlobalData.sessions.remove(source)


def handle_packet(payload):
    
    header = GlobalData.header

    packet_type = header.packet_type

    if packet_type == packet_types['keepalive']:
        keep_alive(header)
        return

    if packet_type == packet_types['route_update']:
        route_update(header, payload)
        return

    if packet_type == packet_types['full_table_request']:
        full_table_request(header.source)
        return

    if packet_type == packet_types['full_table_update']:
        full_table_update(header.source, header.flag, payload)
        return

    if packet_type == packet_types['send_request_identity']:
        send_request_identity(header, payload)
        return
    
    if packet_type == packet_types['group_message']:
        group_message(payload, header)
        return

    if packet_type == packet_types['screen_message']:
        screen_message(header, payload)
        return

    if packet_type == packet_types['metadata_message']:
        metadata_message(header, payload)
        return

