#! /usr/bin/python3

import time
import constants as c
from packet import create_packet

class UserMessageACK:
    def __init__(self):
        self.user_messages = {}
    
    def add(self, user_id, sequance_number):
        
        if (user_id in self.user_messages.keys()):  
            self.user_messages[user_id][sequance_number] = time.time()
        else:
            self.user_messages[user_id] = { sequance_number : time.time() }

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

    def get(self, user_id):

        return self.message_sn[user_id]


def send_message(sock, sessions, sequances, packet_type, flag, destination, payload):

    session_id = -1

    if (flag == c.FLAG_TYPE['single_packet']):
        session_id = 0

    if (flag == c.FLAG_TYPE['normal'] or flag == c.FLAG_TYPE['last_packet']):
        session_id = sessions.get_sessions(destination)

    if (flag == c.FLAG_TYPE['first_packet']):
        session_id = sessions.get_new_session(destination)

    sequances.add(destination, len(payload))
    sequance_number = sequances.get(destination)


    packet = create_packet(c.PROTOCOL_VERSION, packet_type, flags, c.SERVER_KEY, destination, session_id, sequance_number, payload)

    address = get_next_dest(destination)

    print('Sending massage to', address.nickname)

    sock.sendto(packet, (address.ip, address.port))