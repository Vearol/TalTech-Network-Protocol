#! /usr/bin/python3

import time

from message import Message
from global_data import GlobalData
from global_config import KEEPALIVE_LIMIT, MAX_ROUTE_COST, packet_types
from byte_parser import GPG_to_bytes, number_to_bytes
from colors import colors


class Keepalive:

    def __init__(self, nodes):
        self.user_keepalives = dict.fromkeys(nodes.get_neighbors(), time.time())

       
    def update_user(self, user_id):
        
        self.user_keepalives[user_id] = time.time()


    def update_online_users_status(self):
        now = time.time()
        neighbors = GlobalData.nodes.get_neighbors()

        for key, value in self.user_keepalives.items():
            if (now - value > KEEPALIVE_LIMIT):
                # send neighbors update about dead user
                log = key + ' didn\'t update its status for ' + str(KEEPALIVE_LIMIT) + 'sec. Considered offline.'
                print(colors.LOG, log)
                payload = bytearray(10)
                payload[0:8] = GPG_to_bytes(key)
                payload[8:] = number_to_bytes(MAX_ROUTE_COST, 2)
                
                Message.send_message_to_group(packet_types['route_update'], neighbors, payload)

    
    def send(self):

        neighbors = GlobalData.nodes.get_neighbors()
        Message.send_message_to_group(packet_types['keepalive'], neighbors, bytes(0))