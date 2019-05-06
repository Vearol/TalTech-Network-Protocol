#! /usr/bin/python3

from global_config import HEADER_BUFFER, MAX_SN

# sequence number storage
class UserMessageSN:
    def __init__(self):
        self.out_message_sn = {}
        self.in_message_sn = {}
    
    def add_out(self, user_id, session_id, sequence_number):
        
        user_id = user_id.lower()

        if (user_id in self.out_message_sn.keys()):  
            self.out_message_sn[user_id][session_id] += sequence_number
        else:
            self.out_message_sn[user_id] = { session_id : sequence_number }

        if (self.out_message_sn[user_id][session_id] > MAX_SN):
                self.out_message_sn[user_id][session_id] -= MAX_SN


    def get_out(self, user_id, session_id):

        key = user_id.lower()

        if (key in self.out_message_sn.keys()):
            return self.out_message_sn[key][session_id]
        
        return 0
    

    def add_in(self, user_id, session_id, sequence_number):

        user_id = user_id.lower()
        
        if (user_id in self.in_message_sn.keys()):  
            self.in_message_sn[user_id][session_id] += sequence_number
        else:
            self.in_message_sn[user_id] = { session_id : sequence_number }

        if (self.in_message_sn[user_id] > MAX_SN):
                self.in_message_sn[user_id] -= MAX_SN


    def get_in(self, user_id, session_id):

        key = user_id.lower()

        if (key in self.in_message_sn.keys()):
            return self.in_message_sn[key][session_id]
        
        return 0
