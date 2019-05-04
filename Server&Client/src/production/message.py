#! /usr/bin/python3

import time
from queue import Queue

from global_config import *
from global_data import GlobalData
from packet import create_packet
from files import generate_file_metadata
from byte_parser import number_to_bytes
from colors import colors


class UserMessageACK:
    
    def __init__(self):
        self.user_messages = {}
        self.user_acks = {}
    
    # TODO clean this garbage once in a while!!!! in case remove is not called

    # track of outcoming messages with time, to check ACK. user_id - destination
    def add(self, user_id, sequence_number, payload):
        user_id = user_id.lower()
        if (user_id in self.user_messages.keys()):  
            self.user_messages[user_id][sequence_number] = [time.time(), payload]
        else:
            self.user_messages[user_id] = { sequence_number : [time.time(), payload] }

    def add_ack(self, user_id, sequence_number):
        user_id = user_id.lower()
        if (user_id not in self.user_acks.keys()):  
            self.user_acks[user_id] = Queue()

        self.user_acks[user_id].put(sequence_number)


    def get_ack(self, user_id):
        user_id = user_id.lower()
        if (user_id not in self.user_acks.keys()):
            log = 'Cannot find user ' + user_id + ' in ACK queue'
            print(colors.ERROR, log)
            return -1

        if (self.user_acks[user_id].empty()):
            log = 'No pending ACKs for ' + user_id
            print(colors.ERROR, log)
            return -1

        return self.user_acks[user_id].get()


    def get_packet(self, user_id, sequence_number):
        user_id = user_id.lower()
        if (user_id in self.user_messages.keys()):
            if (sequence_number in self.user_messages[user_id].keys()):
                return self.user_messages[user_id][sequence_number][1]
            
            else:
                log = 'Cannot find packet with seq.number: ' + str(sequence_number) + ' for user: ' + user_id
                print(colors.ERROR, log)
                return []
        else:
            log = 'Cannot find any packet for user: ' + user_id
            print(colors.ERROR, log)
            return []


    # remove from tracking, when 
    def remove(self, user_id, sequence_number):
        user_id = user_id.lower()
        if (user_id in self.user_messages.keys()):  
            self.user_messages[user_id].pop(sequence_number)



class Message:

    # send usual packets
    @staticmethod
    def send_message(packet_type, destination, payload):

        session_id = GlobalData.sessions.get_new_session(destination)
        ip, port = GlobalData.nodes.get_network_info(destination)

        size = len(payload)

        flag = flag_types['single_packet']

        if (size > PAYLOAD_BUFFER):
            flag = flag_types['first_packet']
        else:
            GlobalData.sequences.add_out(destination, size)
            sequence_number = GlobalData.sequences.get_out(destination)
        
            packet = create_packet(PROTOCOL_VERSION, packet_type, flag, SERVER_KEY, destination, session_id, sequence_number, payload)

            with GlobalData.lock:
                GlobalData.sock.sendto(packet, (ip, port))
                # GlobalData.sock.sendto(packet, (DEFAULT_DEST_IP, DEFAULT_DEST_PORT))

            GlobalData.messages.add(destination, sequence_number, payload)
            GlobalData.messages.add_ack(destination, sequence_number)

            return

        chunks = int(size / PAYLOAD_BUFFER)

        for i in range(chunks):
            range_from = i * PAYLOAD_BUFFER
            range_to = range_from + PAYLOAD_BUFFER

            GlobalData.sequences.add_out(destination, PAYLOAD_BUFFER)
            sequence_number = GlobalData.sequences.get_out(destination)

            packet = create_packet(PROTOCOL_VERSION, packet_type, flag, SERVER_KEY, destination, session_id, sequence_number, payload[range_from:range_to])

            with GlobalData.lock:
                GlobalData.sock.sendto(packet, (ip, port))
                # GlobalData.sock.sendto(packet, (DEFAULT_DEST_IP, DEFAULT_DEST_PORT))

            flag = flag_types['normal']
            GlobalData.messages.add(destination, sequence_number, payload[range_from:range_to])
            GlobalData.messages.add_ack(destination, sequence_number)

        flag = flag_types['last_packet']

        data_sent = PAYLOAD_BUFFER * chunks

        GlobalData.sequences.add_out(destination, size - data_sent)
        sequence_number = GlobalData.sequences.get_out(destination)

        packet = create_packet(PROTOCOL_VERSION, packet_type, flag, SERVER_KEY, destination, session_id, sequence_number, payload[data_sent:])

        with GlobalData.lock:
            GlobalData.sock.sendto(packet, (ip, port))

        GlobalData.messages.add(destination, sequence_number, payload[data_sent:])
        GlobalData.messages.add_ack(destination, sequence_number)


    # sending files
    @staticmethod
    def send_file(destination, file_path):

        packet_type = packet_types['metadata_message']
        session_id = GlobalData.sessions.get_new_session(destination)
        
        ip, port = GlobalData.nodes.get_network_info(destination)

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

            GlobalData.sequences.add_out(destination, len(data))
            sequence_number = GlobalData.sequences.get_out(destination)

            packet = create_packet(PROTOCOL_VERSION, packet_type, flag, SERVER_KEY, destination, session_id, sequence_number, data)
            
            with GlobalData.lock:
                GlobalData.sock.sendto(packet, (ip, port))
                # GlobalData.sock.sendto(packet, (DEFAULT_DEST_IP, DEFAULT_DEST_PORT))

            GlobalData.messages.add(destination, sequence_number, data)
            GlobalData.messages.add_ack(destination, sequence_number)     
            
            file_data = file_to_send.read(PAYLOAD_BUFFER - METADATA_HEADER)
            data = number_to_bytes(0, METADATA_HEADER) + file_data
                
            flag = flag_types['normal']
                
            if (len(data) < PAYLOAD_BUFFER):
                flag = flag_types['last_packet']            
            
        file_to_send.close()


    # resend lost packets
    @staticmethod
    def resend_message(packet_type, destination, payload):

        flag = flag_types['single_packet']

        sequence_number = GlobalData.sequences.get_out(destination)
        
        packet = create_packet(PROTOCOL_VERSION, packet_type, flag, SERVER_KEY, destination, 0, sequence_number, payload)

        ip, port = GlobalData.nodes.get_network_info(destination)
        with GlobalData.lock:
            GlobalData.sock.sendto(packet, (ip, port))


    # ACK message
    @staticmethod
    def send_ACK(packet_type, sequence_number, destination):

        local_sequence_number = GlobalData.sequences.get_in(destination)

        packet = []

        if (local_sequence_number == sequence_number):
            packet = create_packet(PROTOCOL_VERSION, packet_type, flag_types['ACK'], SERVER_KEY, DEFAULT_DESTINATION, 0, local_sequence_number, bytes(0))
            print(colors.LOG, 'Sending ACK to', destination)
        else:
            missed_sequence_number = sequence_number - local_sequence_number
            
            packet = create_packet(PROTOCOL_VERSION, packet_type, flag_types['NOT_ACK'], SERVER_KEY, DEFAULT_DESTINATION, 0, missed_sequence_number, bytes(0))
            print(colors.LOG, 'Sending NOT_ACK to', destination)

        with GlobalData.lock:
            ip, port = GlobalData.nodes.get_network_info(destination)
            GlobalData.sock.sendto(packet, (ip, port))
            # GlobalData.sock.sendto(packet, (DEFAULT_DEST_IP, DEFAULT_DEST_PORT))


    # Forwarding
    @staticmethod
    def forward(message, destination):
    
        ip, port = GlobalData.nodes.get_network_info(destination)

        print(colors.LOG, 'Forwarding massage to', ip)

        GlobalData.sock.sendto(message, (ip, port))