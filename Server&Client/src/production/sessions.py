#! /usr/bin/python3

class UserSessions:
    
    def __init__(self):
        # data from incoming messages. source : [payload]
        self.user_data = {}

        # track of outcoming session autoincrement
        self.user_sessions = {}
    

    def add(self, user_id, payload):
        
        if (user_id in self.user_data.keys()):
            self.user_data[user_id].append(payload)
        else:
            self.user_data[user_id] = [payload]
    

    def remove(self, user_id):
        
        if (user_id in self.user_data.keys()):  
            self.user_data.pop(user_id)


    def get_new_session(self, user_id):

        if (user_id in self.user_sessions.keys()):
            self.user_sessions[user_id] += 1
        else:
            self.user_sessions[user_id] = 1
        
        return self.user_sessions[user_id]
    

    def get_session(self, user_id):

        if (user_id in self.user_sessions.keys()):
            return self.user_sessions[user_id]
        else:
            self.user_sessions[user_id] = 1
        
        return 1