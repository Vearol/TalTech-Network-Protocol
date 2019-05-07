#! /usr/bin/python3

import json

from global_config import packet_types, flag_types, FILENAME_KEY, FILESIZE_KEY, SERVER_KEY, ID_KEY, RESPONCE_KEY, NAME_KEY
from global_data import GlobalData
from message import Message
from byte_parser import bytes_to_number
from files import parse_file_metadata
from colors import colors


def keep_alive(header):
    
    Message.send_ACK(header.packet_type, header.seqence_number, 0, header.source)


def route_update(payload):
   
    print(colors.LOG, 'route update message')
    # do something


def full_table_request(destination):
    
    print(colors.LOG, 'request full active routing table message')
    # TODO check data format
    payload = GlobalData.nodes.get_full_table_byte()

    Message.send_message(packet_types['full_table_update'], destination, payload)


def full_table_update(source, flag, payload):

    print(colors.LOG, 'full table update message')

    GlobalData.nodes.remove_table(source)

    if (header.flag == flag_types['single_packet']):
        GlobalData.nodes.add_table_byte(payload)
        return
    
    payload_data = GlobalData.sessions.get_data(source)

    GlobalData.nodes.add_table_byte(payload_data)


def send_request_identity(payload, header):
    
    identity_data = json.load(payload.decode())

    GlobalData.nodes.set_nickname(header.source, identity_data[NAME_KEY])

    responce_required = bool(identity_data[RESPONCE_KEY])
    if (responce_required):

        server_name = GlobalData.nodes.get_nickname(SERVER_KEY)

        server_data = {
            ID_KEY : SERVER_KEY,
            RESPONCE_KEY : 'false',
            NAME_KEY : server_name
        }

        server_data_bytes = json.dumps(server_data).encode()

        GlobalData.messages.send_message(header.packet_type, header.source, server_data_bytes)



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
        route_update(payload)
        return

    if packet_type == packet_types['full_table_request']:
        full_table_request(header.source)
        return

    if packet_type == packet_types['full_table_update']:
        full_table_update(header.source, header.flag, payload)
        return

    if packet_type == packet_types['send_request_identity']:
        send_request_identity(payload, header)
        return

    if packet_type == packet_types['screen_message']:
        screen_message(header, payload)
        return

    if packet_type == packet_types['metadata_message']:
        metadata_message(header, payload)
        return

