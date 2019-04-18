#! /usr/bin/python3

import time

class UserMeesageACK:
    def __init__(self):
        self.user_messages = {}
    
    def add(self, user_id, sequance_number):
        
        if (user_id in self.user_messages.keys()):  
            self.user_messages[user_id][sequance_number] = time.time()
        else:
            self.user_messages[key] = { sequance_number : time.time() }

    def remove(self, user_id, sequance_number):
        if (user_id in self.user_messages.keys()):  
            self.user_messages[user_id].pop(sequance_number)