#! /usr/bin/python3

from global_config import packet_types, flag_types, METADATA_HEADER
from global_data import GlobalData
from packet import create_packet
from message import Message
from byte_parser import bytes_to_number
from colors import colors


def skip_index(payload, packet_type):
    
    if (packet_type == packet_types['metadata_message']):
        return METADATA_HEADER + bytes_to_number(payload[0 : METADATA_HEADER])
    
    return 0


def normal(source, packet_type, payload):
    
    skip = skip_index(payload, packet_type)
    GlobalData.sessions.add(source, payload[skip:])

    Message.send_ACK(packet_type, source)


def first_packet(source, packet_type, payload):
   
    GlobalData.sessions.add(source, payload)

    Message.send_ACK(packet_type, source)


def last_packet(source, packet_type, payload):
    
    skip = skip_index(payload, packet_type)
    GlobalData.sessions.add(source, payload[skip:])

    Message.send_ACK(packet_type, source)


def single_packet(packet_type, source):
   
    Message.send_ACK(packet_type, source)


def ACK(source, sequence_number):
    
    print(colors.LOG, 'Received ACK from', source)
    GlobalData.messages_ack.remove(source, sequence_number)
    
    local_sequance_number = GlobalData.sequences.get_out(source)
    if (sequence_number != local_sequance_number):
        print(colors.ERROR, 'Sequance number missmatch in ACK')


def NOT_ACK():
    pass
    # TODO resend some packet?


def error():
    pass
    # do something


def handle_flag(payload):
    
    header = GlobalData.header_parser

    # add incoming seqance number no matter what
    GlobalData.sequences.add_in(header.source, len(payload))

    flag = header.flag

    if flag == flag_types['normal']:
        normal(header.source, header.packet_type, payload)
        return

    if flag == flag_types['first_packet']:
        first_packet(header.source, header.packet_type, payload)
        return

    if flag == flag_types['last_packet']:
        last_packet(header.source, header.packet_type, payload)
        return

    if flag == flag_types['single_packet']:
        single_packet(header.packet_type, header.source)
        return

    if flag == flag_types['ACK']:
        ACK(header.source, header.sequence_number)
        return

    if flag == flag_types['NOT_ACK']:
        NOT_ACK()
        return

    if flag == flag_types['error']:
        error()
        return

