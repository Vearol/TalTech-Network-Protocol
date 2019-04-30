#! /usr/bin/python3

from global_mapping import packet_types, flag_types, METADATA_HEADER
from packet import create_packet
from message import send_ACK
from byte_parser import bytes_to_number
from colors import colors


def skip_index(payload, packet_type):
    
    if (packet_type == packet_types['metadata_message']):
        return METADATA_HEADER + bytes_to_number(payload[0 : METADATA_HEADER])
    
    return 0


def normal(sessions, source, packet_type, payload):
    
    skip = skip_index(payload, packet_type)
    sessions.add(source, payload[skip:])


def first_packet(sessions, source, payload):
   
    sessions.add(source, payload)


def last_packet(sock, sessions, source, packet_type, sequences, payload):
    
    skip = skip_index(payload, packet_type)
    sessions.add(source, payload[skip:])

    send_ACK(sock, packet_type, source, sequences)


def single_packet(sock, packet_type, source, sequences):
   
    send_ACK(sock, packet_type, source, sequences)


def ACK(user_messages, source, sequence_number, sequences):
    
    print(colors.LOG, 'Received ACK from', source)
    user_messages.remove(source, sequence_number)
    
    local_sequance_number = sequences.get_out(source)
    if (sequence_number != local_sequance_number):
        print(colors.ERROR, 'Sequance number missmatch in ACK')


def NOT_ACK():
    pass
    # TODO resend some packet?


def error():
    pass
    # do something


def handle_flag(sock, sessions, sequances, user_messages, header, payload):
    
    # add incoming seqance number no matter what
    sequances.add_in(header.source, len(payload))

    flag = header.flag

    if flag == flag_types['normal']:
        normal(sessions, header.source, header.packet_type, payload)
        return

    if flag == flag_types['first_packet']:
        first_packet(sessions, header.source, payload)
        return

    if flag == flag_types['last_packet']:
        last_packet(sock, sessions, header.source, header.packet_type, sequances, payload)
        return

    if flag == flag_types['single_packet']:
        single_packet(sock, header.packet_type, header.source, sequances)
        return

    if flag == flag_types['ACK']:
        ACK(user_messages, header.source, header.sequence_number, sequances)
        return

    if flag == flag_types['NOT_ACK']:
        NOT_ACK()
        return

    if flag == flag_types['error']:
        error()
        return

