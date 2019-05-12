#! /usr/bin/python3

import time
import json
from queue import Queue

from global_config import *
from global_data import GlobalData
from packet import create_packet
from json_parser import generate_file_metadata, generate_identity_bytes
from byte_parser import number_to_bytes
from colors import colors


class UserMessageACK:
    
    def __init__(self):
        self.user_messages = {}
        self.user_acks = {}
        self.resend_timeouts = {}
    
    # TODO clean this garbage once in a while!!!! in case remove is not called

    # track of outcoming messages with time, to check ACK. user_id - destination
    def add(self, user_id, session_id, sequence_number, packet_type, payload):
        user_id = user_id.lower()
        if (user_id in self.user_messages.keys()): 
            if (session_id in self.user_messages[user_id].keys()):
                self.user_messages[user_id][session_id][sequence_number] = [packet_type, time.time(), payload]
            else:
               self.user_messages[user_id][session_id] = { sequence_number : [packet_type, time.time(), payload] }
        else:
            self.user_messages[user_id] = { session_id : { sequence_number : [packet_type, time.time(), payload] } }


    def get_packet(self, user_id, session_id, sequence_number):
        user_id = user_id.lower()
        if (user_id in self.user_messages.keys()):
            if (session_id in self.user_messages[user_id].keys()):
                if (sequence_number in self.user_messages[user_id][session_id].keys()):
                    message_data = self.user_messages[user_id][session_id][sequence_number]
                    return (message_data[0], message_data[2])
                else:
                    # getting whole session
                    payload = []
                    packet_type = 0
                    if (sequence_number == 0):
                        for data in self.user_messages[user_id][session_id].values():
                            payload.append(data[2])
                            packet_type = data[0]

                        return (packet_type, payload)

                    return (0, [])    
            else:
                log = 'Cannot find packet with session id: ' + str(session_id) + ' for user: ' + user_id
                print(colors.ERROR, log)
                return (0, [])
        else:
            log = 'Cannot find any packet for user: ' + user_id
            print(colors.ERROR, log)
            return (0, [])


    def get_pending_sessions(self, user_id):
        now = time.time()
        if (user_id in self.resend_timeouts.keys() and now - self.resend_timeouts[user_id] < RESEND_TIMEOUT_SEC):
            return []

        self.resend_timeouts[user_id] = now

        pending_sessions = []
        for key, value in self.user_acks[user_id].items():
            if not value.empty():
                pending_sessions.append(key)

        return pending_sessions


    def add_ack(self, user_id, session_id, sequence_number):
        user_id = user_id.lower()
        if (user_id not in self.user_acks.keys()):  
            self.user_acks[user_id] = { session_id : Queue() }

        if (session_id not in self.user_acks[user_id].keys()):  
            self.user_acks[user_id][session_id] = Queue()

        self.user_acks[user_id][session_id].put(sequence_number)


    def get_ack(self, user_id, session_id):
        user_id = user_id.lower()
        if (user_id not in self.user_acks.keys()):
            log = 'Cannot find user ' + user_id + ' in ACK queue'
            print(colors.ERROR, log)
            return -1

        if (session_id not in self.user_acks[user_id].keys()):
            log = 'Cannot find session ' + str(session_id) + ' for user ' + user_id + ' in ACK queue'
            print(colors.ERROR, log)
            return -1

        if (self.user_acks[user_id][session_id].empty()):
            log = 'No pending ACKs for ' + user_id + ' in session ' + str(session_id)
            print(colors.ERROR, log)
            return -1

        return self.user_acks[user_id][session_id].get()


    # remove from tracking, when ACK
    def remove(self, user_id, session_id):
        user_id = user_id.lower()
        if (user_id in self.user_messages.keys()):
            if (session_id in self.user_messages[user_id].keys()):
                self.user_messages[user_id].pop(session_id)


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
            GlobalData.sequences.add_out(destination, session_id, size)
            sequence_number = GlobalData.sequences.get_out(destination, session_id)
        
            packet = create_packet(PROTOCOL_VERSION, packet_type, flag, SERVER_KEY, destination, 
                                   session_id, sequence_number, payload)

            with GlobalData.lock:
                GlobalData.sock.sendto(packet, (ip, port))
            
            GlobalData.messages.add(destination, session_id, sequence_number, packet_type, payload)
            GlobalData.messages.add_ack(destination, session_id, sequence_number)

            return

        chunks = int(size / PAYLOAD_BUFFER)

        for i in range(chunks):
            range_from = i * PAYLOAD_BUFFER
            range_to = range_from + PAYLOAD_BUFFER

            GlobalData.sequences.add_out(destination, session_id, PAYLOAD_BUFFER)
            sequence_number = GlobalData.sequences.get_out(destination, session_id)

            packet = create_packet(PROTOCOL_VERSION, packet_type, flag, SERVER_KEY, destination, 
                                   session_id, sequence_number, payload[range_from:range_to])

            with GlobalData.lock:
                GlobalData.sock.sendto(packet, (ip, port))

            flag = flag_types['normal']
            GlobalData.messages.add(destination, session_id, sequence_number, packet_type, payload[range_from:range_to])
            GlobalData.messages.add_ack(destination, session_id, sequence_number)

        flag = flag_types['last_packet']

        data_sent = PAYLOAD_BUFFER * chunks

        GlobalData.sequences.add_out(destination, session_id, size - data_sent)
        sequence_number = GlobalData.sequences.get_out(destination, session_id)

        packet = create_packet(PROTOCOL_VERSION, packet_type, flag, SERVER_KEY, destination, 
                               session_id, sequence_number, payload[data_sent:])

        with GlobalData.lock:
            GlobalData.sock.sendto(packet, (ip, port))

        GlobalData.messages.add(destination, session_id, sequence_number, packet_type, payload[data_sent:])
        GlobalData.messages.add_ack(destination, session_id, sequence_number)


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

            GlobalData.sequences.add_out(destination, session_id, len(data))
            sequence_number = GlobalData.sequences.get_out(destination, session_id)

            packet = create_packet(PROTOCOL_VERSION, packet_type, flag, SERVER_KEY, destination, 
                                   session_id, sequence_number, data)
            
            with GlobalData.lock:
                GlobalData.sock.sendto(packet, (ip, port))

            GlobalData.messages.add(destination, session_id, sequence_number, packet_type, data)
            GlobalData.messages.add_ack(destination, session_id, sequence_number)     
            
            file_data = file_to_send.read(PAYLOAD_BUFFER - METADATA_HEADER)
            data = number_to_bytes(0, METADATA_HEADER) + file_data
                
            flag = flag_types['normal']
                
            if (len(data) < PAYLOAD_BUFFER):
                flag = flag_types['last_packet']            
            
        file_to_send.close()


    # resend single message
    @staticmethod
    def resend_message(packet_type, session_id, destination, payload, whole_session=False):

        ip, port = GlobalData.nodes.get_network_info(destination)

        if (whole_session):
            packets_count = len(payload)

            if (packets_count > 1):
                flag = flag_types['first_packet']
                sequence_number = 0

                for packet in range(packets_count - 1):
                    data = payload[packet]
                    sequence_number += len(data)
                    packet = create_packet(PROTOCOL_VERSION, packet_type, flag, SERVER_KEY, destination, 
                                           session_id, sequence_number, data)

                    with GlobalData.lock:
                        GlobalData.sock.sendto(packet, (ip, port))
                    
                    flag = flag_types['normal']
                
                flag = flag_types['last_packet']
                data = payload[packets_count - 1]
                sequence_number += len(data)
                packet = create_packet(PROTOCOL_VERSION, packet_type, flag, SERVER_KEY, destination, 
                                       session_id, sequence_number, data)

                with GlobalData.lock:
                    GlobalData.sock.sendto(packet, (ip, port))
            
                return
            
            if (len(payload) > 0):
                payload = payload[0]

        
        flag = flag_types['single_packet']

        sequence_number = GlobalData.sequences.get_out(destination, session_id)
        
        packet = create_packet(PROTOCOL_VERSION, packet_type, flag, SERVER_KEY, destination, 
                               session_id, sequence_number, payload)

        with GlobalData.lock:
            GlobalData.sock.sendto(packet, (ip, port))


    # resend all unacknowledged messages
    @staticmethod
    def resend_pending_messages(destination):
        pending_sessions = GlobalData.messages.get_pending_sessions(destination)

        for session_id in pending_sessions:
            packet_type, payload = GlobalData.messages.get_packet(destination, session_id, 0)

            Message.resend_message(packet_type, session_id, destination, payload, True)


    # ACK message
    @staticmethod
    def send_ACK():

        header = GlobalData.header
        
        session_id = header.session_id
        destination = header.source
        sequence_number = header.sequence_number
        packet_type = header.packet_type

        local_session_id = GlobalData.sessions.get_income_session(destination)
        local_sequence_number = GlobalData.sequences.get_in(destination, local_session_id)

        ip, port = GlobalData.nodes.get_network_info(destination)

        packet = []

        if (local_session_id == session_id and local_sequence_number == sequence_number):
            packet = create_packet(PROTOCOL_VERSION, packet_type, flag_types['ACK'], SERVER_KEY, destination, 
                                   session_id, local_sequence_number, bytes(0))
            print(colors.LOG, 'Sending ACK to', destination)
            
            with GlobalData.lock:
                GlobalData.sock.sendto(packet, (ip, port))
            return
        
        if (local_session_id == session_id and local_sequence_number != sequence_number):
            missed_sequence_number = sequence_number - local_sequence_number
            
            packet = create_packet(PROTOCOL_VERSION, packet_type, flag_types['NOT_ACK'], SERVER_KEY, destination, 
                                   session_id, missed_sequence_number, bytes(0))
            print(colors.LOG, 'Sending NOT_ACK to', destination)
            
            with GlobalData.lock:
                GlobalData.sock.sendto(packet, (ip, port))
            return

        packet = create_packet(PROTOCOL_VERSION, packet_type, flag_types['ACK'], SERVER_KEY, destination, 
                               local_session_id, local_sequence_number, bytes(0))
        log = 'Sending ACK of missed session ' + str(session_id) + ', seq.num: ' + str(sequence_number) + ' to ' + destination
        print(colors.LOG, log)
            
        with GlobalData.lock:
            GlobalData.sock.sendto(packet, (ip, port))

        if (local_session_id != session_id):
            packet = create_packet(PROTOCOL_VERSION, packet_type, flag_types['NOT_ACK'], SERVER_KEY, destination, 
                                   session_id, sequence_number, bytes(0))
            print(colors.LOG, 'Sending NOT_ACK to', destination)
            
            with GlobalData.lock:
                GlobalData.sock.sendto(packet, (ip, port))


    # Forwarding
    @staticmethod
    def forward(message, destination):
    
        ip, port = GlobalData.nodes.get_network_info(destination)

        print(colors.LOG, 'Forwarding massage to', ip)

        with GlobalData.lock:
            GlobalData.sock.sendto(message, (ip, port))


    # Fake ACK for group messages... TODO
    @staticmethod
    def send_fake_ACK():

        header = GlobalData.header

        ip, port = GlobalData.nodes.get_network_info(header.destination)

        packet = create_packet(PROTOCOL_VERSION, header.packet_type, flag_types['ACK'], SERVER_KEY, header.destination, 
                               header.session_id, header.sequence_number, bytes(0))

        with GlobalData.lock:
            GlobalData.sock.sendto(packet, (ip, port))

    # send a copy of message with same packet type and payload to multiple users
    @staticmethod
    def send_message_to_group(packet_type, destination_array, payload):
        
        for destination in destination_array:
            Message.send_message(packet_type, destination, payload)


    @staticmethod
    def send_identity_request(destination):

        server_identity = generate_identity_bytes('true')

        Message.send_message(packet_types['send_request_identity'], destination, server_identity)