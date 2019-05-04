#! /usr/bin/python3

from global_config import HEADER_BUFFER, MAX_SN

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
