#! /usr/bin/python3

import time

from global_mapping import *
from packet import create_packet
from files import generate_file_metadata
from byte_parser import number_to_bytes
from colors import colors


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
        self.out_message_sn = {}
        self.in_message_sn = {}
    
    def add_out(self, user_id, sequence_number):
        
        key = user_id.lower()

        if (key in self.out_message_sn.keys()):  
            self.out_message_sn[key] += sequence_number
        else:
            self.out_message_sn[key] = sequence_number

        if (self.out_message_sn[key] > MAX_SN):
                self.out_message_sn[key] -= MAX_SN


    def get_out(self, user_id):

        key = user_id.lower()

        if (key in self.out_message_sn.keys()):
            return self.out_message_sn[key]
        
        self.out_message_sn[key] = 0
        return 0
    

    def add_in(self, user_id, sequence_number):

        key = user_id.lower()
        
        if (key in self.in_message_sn.keys()):  
            self.in_message_sn[key] += sequence_number
        else:
            self.in_message_sn[key] = sequence_number

        if (self.in_message_sn[key] > MAX_SN):
                self.in_message_sn[key] -= MAX_SN


    def get_in(self, user_id):

        key = user_id.lower()

        if (key in self.in_message_sn.keys()):
            return self.in_message_sn[key]
        
        self.in_message_sn[key] = 0
        return 0


# send usual packets
def send_message(sock, sessions, sequences, messages_ack, packet_type, destination, payload):

    session_id = sessions.get_new_session(destination)

    size = len(payload)

    flag = flag_types['single_packet']

    if (size > PAYLOAD_BUFFER):
        flag = flag_types['first_packet']
    else:
        sequences.add_out(destination, size)
        sequence_number = sequences.get_out(destination)
        
        packet = create_packet(PROTOCOL_VERSION, packet_type, flag, SERVER_KEY, destination, session_id, sequence_number, payload)

        sock.sendto(packet, (DEFAULT_DEST_IP, DEFAULT_DEST_PORT))

        return

    chunks = int(size / PAYLOAD_BUFFER)

    for i in range(chunks):
        range_from = i * PAYLOAD_BUFFER
        range_to = range_from + PAYLOAD_BUFFER

        sequences.add_out(destination, PAYLOAD_BUFFER)
        sequence_number = sequences.get_out(destination)

        packet = create_packet(PROTOCOL_VERSION, packet_type, flag, SERVER_KEY, destination, session_id, sequence_number, payload[range_from:range_to])

        sock.sendto(packet, (DEFAULT_DEST_IP, DEFAULT_DEST_PORT))

        flag = flag_types['normal']
        sequence_number.add(destination, PAYLOAD_BUFFER)

    flag = flag_types['last_packet']

    data_sent = PAYLOAD_BUFFER * chunks

    sequences.add_out(destination, size - data_sent)
    sequence_number = sequences.get_out(destination)

    packet = create_packet(PROTOCOL_VERSION, packet_type, flag, SERVER_KEY, destination, session_id, sequence_number, payload[data_sent:])

    sock.sendto(packet, (DEFAULT_DEST_IP, DEFAULT_DEST_PORT))

    messages_ack.add(destination, sequence_number)


# sending files
def send_file(sock, sessions, sequences, messages_ack, packet_type, destination, file_path):

    session_id = sessions.get_new_session(destination)

    metadata, file_size = generate_file_metadata(file_path)

    file_to_send = open(file_path, "rb")

    metadata_length = len(metadata)
    metadata_header = number_to_bytes(metadata_length, METADATA_HEADER)

    # possible negative value
    file_data = file_to_send.read(PAYLOAD_BUFFER - METADATA_HEADER - metadata_length)
    data = metadata_header + metadata + file_data

    size = file_size + metadata_length + METADATA_HEADER
    
    flag = flag_types['single_packet']
    if (size > PAYLOAD_BUFFER):
        flag = flag_types['first_packet']

    while (file_data):

        sequences.add_out(destination, len(data))
        sequence_number = sequences.get_out(destination)

        packet = create_packet(PROTOCOL_VERSION, packet_type, flag, SERVER_KEY, destination, session_id, sequence_number, data)
        
        if ( sock.sendto(packet, (DEFAULT_DEST_IP, DEFAULT_DEST_PORT)) ):
            file_data = file_to_send.read(PAYLOAD_BUFFER - METADATA_HEADER)
            data = number_to_bytes(0, METADATA_HEADER) + file_data
            
            flag = flag_types['normal']
            
            if (len(data) < PAYLOAD_BUFFER):
                flag = flag_types['last_packet']

        messages_ack.add(destination, sequence_number)
        
    file_to_send.close()


# ACK message
def send_ACK(sock, packet_type, destination, sequences):

    sequence_number = sequences.get_in(destination)

    packet = create_packet(PROTOCOL_VERSION, packet_type, flag_types['ACK'], SERVER_KEY, DEFAULT_DESTINATION, 0, sequence_number, bytes(0))

    print(colors.LOG, 'Sending ACK to', destination)
    sock.sendto(packet, (DEFAULT_DEST_IP, DEFAULT_DEST_PORT))
