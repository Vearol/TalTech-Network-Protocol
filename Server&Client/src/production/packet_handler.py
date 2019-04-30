#! /usr/bin/python3

from global_mapping import packet_types, flag_types, FILENAME_KEY, FILESIZE_KEY
from message import send_message
from byte_parser import bytes_to_number
from files import parse_file_metadata


def is_fully_received(flag):

    if (flag == flag_types['normal'] or flag == flag_types['first_packet']):
        return False

    return True

def keep_alive(payload):
    
    print('keep alive message')
    # do something


def route_update(payload):
   
    print('route update message')
    # do something


def full_table_request(sock, sessions, sequences, messages_ack, nodes, destination):
    
    print('request full active routing table message')
    # TODO check data format
    payload = nodes.get_full_table()

    send_message(sock, sessions, sequences, messages_ack, packet_types['full_table_update'], destination, payload)


def full_table_update(flag, nodes, sessions, payload):
   
    if (not is_fully_received(header.flag)):
        return

    print('full table update message')

    if (header.flag == flag_types['single_packet']):
        nodes.update_route_table(payload)
        return
    
    router_data = []
    payload_data = sessions.get_data(source)

    nodes.update_route_table(router_data)


def send_request_identity(payload, header):
    
    print('sent/request identity message')
    # do something


def screen_message(socket, header, sessions, payload):
    
    source = header.source

    # still incoming...
    if (not is_fully_received(header.flag)):
        return

    print('message for screen from', source)

    if (header.flag == flag_types['single_packet']):
        
        message_str = payload.decode('utf-8')    
        print(message_str)
        return

    payload_data = sessions.get_data(source)

    message_str = ''
    for data in payload_data:
        message_str += data.decode('utf-8')
        
    # TODO store in db
    
    print(message_str)


def metadata_message(header, sessions, payload):
    
    source = header.source
    
    # still incoming...
    if (not is_fully_received(header.flag)):
        return
    
    payload_data = payload
    if (header.flag == flag_types['last_packet']):
        payload_data = sessions.get_data(source)

    print('message with binary metadata from', header.source)
    
    metadata, skip = parse_file_metadata(payload_data)

    file_name = 'file_name'
    file_size = 0

    keys = metadata.keys()
    if (FILENAME_KEY in keys):
        file_name = metadata[FILENAME_KEY]
    if (FILESIZE_KEY in keys):
        file_size = metadata[FILESIZE_KEY]

    print('Saving file:', file_name, file_size, 'bytes')

    file_to_save = open(file_name, 'wb')
    
    file_data = payload[skip:]
    file_to_save.write(file_data)

    file_to_save.close()

    sessions.remove(source)


def handle_packet(socket, nodes, sessions, sequences, messages_ack, header, payload):
    
    if (header.flag == flag_types['ACK']):
        return

    packet_type = header.packet_type

    if packet_type == packet_types['keepalive']:
        keep_alive(payload)
        return

    if packet_type == packet_types['route_update']:
        route_update(payload)
        return

    if packet_type == packet_types['full_table_request']:
        full_table_request(sock, sessions, sequences, messages_ack, nodes)
        return

    if packet_type == packet_types['full_table_update']:
        full_table_update(flag, nodes, sessions, payload)
        return

    if packet_type == packet_types['send_request_identity']:
        send_request_identity(payload, header)
        return

    if packet_type == packet_types['screen_message']:
        screen_message(socket, header, sessions, payload)
        return

    if packet_type == packet_types['metadata_message']:
        metadata_message(header, sessions, payload)
        return

