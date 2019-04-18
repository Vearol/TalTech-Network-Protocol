#! /usr/bin/python3

class UserSessions:
    
    def __init__(self):
        self.user_data = {}
    

    def add(self, user_id, payload):
        
        if (user_id in self.user_data.keys()):
            self.user_data[user_id].append(payload)
        else:
            self.user_data[user_id] = [payload]