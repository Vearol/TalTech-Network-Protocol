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
    def add(self, user_id, sequance_number):
        
        if (user_id in self.user_messages.keys()):  
            self.user_messages[user_id][sequance_number] = time.time()
        else:
            self.user_messages[user_id] = { sequance_number : time.time() }


    # remove from tracking, when 
    def remove(self, user_id, sequance_number):
        if (user_id in self.user_messages.keys()):  
            self.user_messages[user_id].pop(sequance_number)


# sequance number storage
class UserMessageSN:
    def __init__(self):
        self.message_sn = {}
    
    def add(self, user_id, sequance_number):
        
        if (user_id in self.message_sn.keys()):  
            self.message_sn[user_id] += sequance_number
        else:
            self.message_sn[user_id] = sequance_number

        if (self.message_sn[user_id] > MAX_SN):
                self.message_sn[user_id] -= MAX_SN

    def get(self, user_id):

        return self.message_sn[user_id]


# send usual packets
def send_message(sock, sessions, sequances, messages_ack, packet_type, destination, payload):

    session_id = sessions.get_new_session(destination)

    size = len(payload)
    address = get_next_dest(destination)

    flag = flag_types['single_packet']

    if (size > PAYLOAD_BUFFER):
        flag = flag_types['first_packet']
    else:
        sequances.add(destination, size)
        sequance_number = sequances.get(destination)

        packet = create_packet(PROTOCOL_VERSION, packet_type, flag, SERVER_KEY, destination, session_id, sequance_number, payload[range_from:range_to])

        sock.sendto(packet, (address.ip, address.port))

        return

    chunks = int(size / PAYLOAD_BUFFER)

    for i in range(chunks):
        range_from = i * PAYLOAD_BUFFER
        range_to = range_from + PAYLOAD_BUFFER

        sequances.add(destination, PAYLOAD_BUFFER)
        sequance_number = sequances.get(destination)

        packet = create_packet(PROTOCOL_VERSION, packet_type, flag, SERVER_KEY, destination, session_id, sequance_number, payload[range_from:range_to])

        sock.sendto(packet, (address.ip, address.port))

        flag = flag_types['normal']
        sequance_number.add(destination, PAYLOAD_BUFFER)

    flag = flag_types['last_packet']

    data_sent = PAYLOAD_BUFFER * chunks

    sequances.add(destination, size - data_sent)
    sequance_number = sequances.get(destination)

    packet = create_packet(PROTOCOL_VERSION, packet_type, flag, SERVER_KEY, destination, session_id, sequance_number, payload[data_sent:])

    address = get_next_dest(destination)

    sock.sendto(packet, (address.ip, address.port))
    messages_ack.add(destination, sequance_number)


# sending files
def send_file(sock, sessions, sequances, messages_ack, packet_type, destination, file_path):

    session_id = get_new_session(destination)

    metadata, file_size = generate_file_metadata(file_path)

    file_to_send = open(file_path, "r")

    metadata_length = len(metadata)
    metadata_header = number_to_bytes(metadata_length, METADATA_HEADER)

    # possible negative value
    data = metadata_header + metadata + file_to_send.read(PAYLOAD_BUFFER - METADATA_HEADER - metadata_length)

    size = file_size + metadata_length + METADATA_HEADER
    
    flag = flag_types['single_packet']
    if (size > PAYLOAD_BUFFER):
        flag = flag_types['first_packet']

    while (data):

        address = get_next_dest(destination)

        sequances.add(destination, len(data))
        sequance_number = sequances.get(destination)

        flag = flag_types['normal']
        if (len(data) < PAYLOAD_BUFFER):
            flag = flag_types['last_packet']

        packet = create_packet(PROTOCOL_VERSION, packet_type, flag, SERVER_KEY, destination, session_id, sequance_number, data)
        
        if ( sock.sendto(packet, (address.ip, address.port)) ):
            data = number_to_bytes(0, METADATA_HEADER) + file_to_send.read(PAYLOAD_BUFFER - metadata_header_length)

        messages_ack.add(destination, sequance_number)
        
    file_to_send.close()


# ACK message
def send_ACK(sock, destination, sequence_number):

    packet = create_packet(PROTOCOL_VERSION, packet_types['metadata_message'], flag_types['ACK'], SERVER_KEY, destination, 0, sequence_number, bytes(0))

    address = get_next_dest(destination)
    sock.sendto(packet, (address.ip, address.port))
