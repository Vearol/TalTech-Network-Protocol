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


def normal(header, payload):
    
    skip = skip_index(payload, header.packet_type)
    GlobalData.sessions.add(header.source, payload[skip:])

    Message.send_ACK(header.packet_type, header.session_id, header.sequence_number, header.source)


def first_packet(header, payload):
   
    GlobalData.sessions.add(header.source, payload)

    Message.send_ACK(header.packet_type, header.session_id, header.sequence_number, header.source)


def last_packet(header, payload):
    
    skip = skip_index(payload, header.packet_type)
    GlobalData.sessions.add(header.source, payload[skip:])

    Message.send_ACK(header.packet_type, header.session_id, header.sequence_number, header.source)


def single_packet(header):
   
    Message.send_ACK(header.packet_type, header.session_id, header.sequence_number, header.source)


def ACK(header):
    
    print(colors.LOG, 'Received ACK from', header.source)
    GlobalData.messages.remove(header.source, header.session_id)
    
    local_sequance_number = GlobalData.messages.get_ack(header.source, header.session_id)

    if (header.sequence_number != local_sequance_number):
        print(colors.ERROR, 'Sequance number missmatch in ACK')


def NOT_ACK(header):

    if (header.sequence_number != 0):
        packet_type, payload = GlobalData.messages.get_packet(header.source, header.session_id, header.sequence_number)
        if (len(payload) == 0):
            return

        Message.resend_message(header.packet_type, header.session_id, header.source, payload, True)
    else:
        Message.resend_pending_messages(header.source)


def error():
    pass
    # do something


def handle_flag(payload):

    header = GlobalData.header

    # group messages... TODO
    if (header.packet_type == packet_types['group_message']):
        Message.send_fake_ACK(header)

    # add incoming seqance number no matter what
    GlobalData.sequences.add_in(header.source, header.session_id, len(payload))

    # inc session if new message:
    if (header.flag == flag_types['first_packet'] or header.flag == flag_types['single_packet']):
        GlobalData.sessions.new_income_session(header.source)

    flag = header.flag

    if flag == flag_types['normal']:
        normal(header, payload)
        return False

    if flag == flag_types['first_packet']:
        first_packet(header, payload)
        return False

    if flag == flag_types['last_packet']:
        last_packet(header, payload)
        return True

    if flag == flag_types['single_packet']:
        single_packet(header)
        return True

    if flag == flag_types['ACK']:
        ACK(header)
        return False

    if flag == flag_types['NOT_ACK']:
        NOT_ACK(header)
        return False

    if flag == flag_types['error']:
        error()
        return False

