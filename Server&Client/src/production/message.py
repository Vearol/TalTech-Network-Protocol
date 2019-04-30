#! /usr/bin/python3

import time

from global_mapping import *
from packet import create_packet
from files import generate_file_metadata
from byte_parser import number_to_bytes


class UserMessageACK:
    
    def __init__(self):
        self.user_messages = {}
    

    # track of outcoming messages with time, to check ACK. user_id - destination
    def add(self, user_id, sequence_number):
        
        if (user_id in self.user_messages.keys()):  
            self.user_messages[user_id][sequence_number] = time.time()
        else:
            self.user_messages[user_id] = { sequence_number : time.time() }


    # remove from tracking, when 
    def remove(self, user_id, sequence_number):
        if (user_id in self.user_messages.keys()):  
            self.user_messages[user_id].pop(sequence_number)


# sequence number storage
class UserMessageSN:
    def __init__(self):
        self.message_sn = {}
    
    def add(self, user_id, sequence_number):
        
        if (user_id in self.message_sn.keys()):  
            self.message_sn[user_id] += sequence_number
        else:
            self.message_sn[user_id] = sequence_number

        if (self.message_sn[user_id] > MAX_SN):
                self.message_sn[user_id] -= MAX_SN

    def get(self, user_id):

        return self.message_sn[user_id]


# send usual packets
def send_message(sock, sessions, sequences, messages_ack, packet_type, destination, payload):

    session_id = sessions.get_new_session(destination)

    size = len(payload)
    address_ip = '193.40.103.97'
    address_port = 8088

    flag = flag_types['single_packet']

    if (size > PAYLOAD_BUFFER):
        flag = flag_types['first_packet']
    else:
        sequences.add(destination, size)
        sequence_number = sequences.get(destination)

        packet = create_packet(PROTOCOL_VERSION, packet_type, flag, SERVER_KEY, destination, session_id, sequence_number, payload)

        sock.sendto(packet, (DEFAULT_DEST_IP, DEFAULT_DEST_PORT))

        return

    chunks = int(size / PAYLOAD_BUFFER)

    for i in range(chunks):
        range_from = i * PAYLOAD_BUFFER
        range_to = range_from + PAYLOAD_BUFFER

        sequences.add(destination, PAYLOAD_BUFFER)
        sequence_number = sequences.get(destination)

        packet = create_packet(PROTOCOL_VERSION, packet_type, flag, SERVER_KEY, destination, session_id, sequence_number, payload[range_from:range_to])

        sock.sendto(packet, (DEFAULT_DEST_IP, DEFAULT_DEST_PORT))

        flag = flag_types['normal']
        sequence_number.add(destination, PAYLOAD_BUFFER)

    flag = flag_types['last_packet']

    data_sent = PAYLOAD_BUFFER * chunks

    sequences.add(destination, size - data_sent)
    sequence_number = sequences.get(destination)

    packet = create_packet(PROTOCOL_VERSION, packet_type, flag, SERVER_KEY, destination, session_id, sequence_number, payload[data_sent:])

    sock.sendto(packet, (DEFAULT_DEST_IP, DEFAULT_DEST_PORT))
    messages_ack.add(destination, sequence_number)


# sending files
def send_file(sock, sessions, sequences, messages_ack, packet_type, destination, file_path):

    session_id = sessions.get_new_session(destination)

    address_ip = '127.0.0.1'
    address_port = 8088

    metadata, file_size = generate_file_metadata(file_path)

    file_to_send = open(file_path, "rb")

    metadata_length = len(metadata)
    metadata_header = number_to_bytes(metadata_length, METADATA_HEADER)

    # possible negative value
    data = metadata_header + metadata + file_to_send.read(PAYLOAD_BUFFER - METADATA_HEADER - metadata_length)

    size = file_size + metadata_length + METADATA_HEADER
    
    flag = flag_types['single_packet']
    if (size > PAYLOAD_BUFFER):
        flag = flag_types['first_packet']

    while (data):

        sequences.add(destination, len(data))
        sequence_number = sequences.get(destination)

        packet = create_packet(PROTOCOL_VERSION, packet_type, flag, SERVER_KEY, destination, session_id, sequence_number, data)
        
        if ( sock.sendto(packet, (DEFAULT_DEST_IP, DEFAULT_DEST_PORT)) ):
            data = number_to_bytes(0, METADATA_HEADER) + file_to_send.read(PAYLOAD_BUFFER - METADATA_HEADER)
            
            flag = flag_types['normal']
            
            if (len(data) < PAYLOAD_BUFFER):
                flag = flag_types['last_packet']

        messages_ack.add(destination, sequence_number)
        
    file_to_send.close()


# ACK message
def send_ACK(sock, destination, sequence_number):

    packet = create_packet(PROTOCOL_VERSION, packet_types['metadata_message'], flag_types['ACK'], DEFAULT_SERVER_GPG, DEFAULT_DESTINATION, 0, sequence_number, bytes(0))

    address_ip = '127.0.0.1'
    address_port = 8088

    sock.sendto(packet, (DEFAULT_DEST_IP, DEFAULT_DEST_PORT))

