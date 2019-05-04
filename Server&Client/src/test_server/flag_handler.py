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


def normal(source, packet_type, sequence_number, payload):
    
    skip = skip_index(payload, packet_type)
    GlobalData.sessions.add(source, payload[skip:])

    Message.send_ACK(packet_type, sequence_number, source, len(payload))


def first_packet(source, packet_type, sequence_number, payload):
   
    GlobalData.sessions.add(source, payload)

    Message.send_ACK(packet_type, sequence_number, source, len(payload))


def last_packet(source, packet_type, sequence_number, payload):
    
    skip = skip_index(payload, packet_type)
    GlobalData.sessions.add(source, payload[skip:])

    Message.send_ACK(packet_type, sequence_number, source, len(payload))


def single_packet(packet_type, sequence_number, source, payload_size):
   
    Message.send_ACK(packet_type, sequence_number, source, payload_size)


def ACK(source, packet_type, sequence_number):
    
    print(colors.LOG, 'Received ACK from', source)
    GlobalData.messages.remove(source, sequence_number)
    
    local_sequance_number = GlobalData.messages.get_ack(source)

    if (sequence_number != local_sequance_number):
        print(colors.ERROR, 'Sequance number missmatch in ACK')


def NOT_ACK(source, packet_type, sequence_number):

    GlobalData.messages.get_ack(source)

    payload = GlobalData.messages.get_packet(source, sequence_number)
    if (len(payload) == 0):
        return

    Message.resend_message(packet_type, source, payload)


def error():
    pass
    # do something


def handle_flag(payload):

    header = GlobalData.header

    # add incoming seqance number no matter what
    GlobalData.sequences.add_in(header.source, len(payload))

    flag = header.flag

    if flag == flag_types['normal']:
        normal(header.source, header.packet_type, header.sequence_number, payload)
        return

    if flag == flag_types['first_packet']:
        first_packet(header.source, header.packet_type, header.sequence_number, payload)
        return

    if flag == flag_types['last_packet']:
        last_packet(header.source, header.packet_type, header.sequence_number, payload)
        return

    if flag == flag_types['single_packet']:
        single_packet(header.packet_type, header.sequence_number, header.source, len(payload))
        return

    if flag == flag_types['ACK']:
        ACK(header.source, header.packet_type, header.sequence_number)
        return

    if flag == flag_types['NOT_ACK']:
        NOT_ACK(header.source, header.packet_type, header.sequence_number)
        return

    if flag == flag_types['error']:
        error()
        return

