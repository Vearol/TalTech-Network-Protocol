#! /usr/bin/python3

from global_mapping import MAX_SESSION

class UserSessions:
    
    def __init__(self):
        # data from incoming messages. source : [payload]
        self.user_data = {}

        # track of outcoming session autoincrement
        self.user_sessions = {}
    

    # add file chunk to local storage, to create file later
    def add(self, user_id, payload):
        
        if (user_id in self.user_data.keys()):
            data = self.user_data[user_id]
            for byte in payload:
                data.append(byte)
        else:
            self.user_data[user_id] = bytearray(payload)
    

    # free the local storage. TODO keep file reference for history
    def remove(self, user_id):
        
        if (user_id in self.user_data.keys()):  
            self.user_data.pop(user_id)


    # generate new autoincrement session id
    def get_new_session(self, user_id):

        if (user_id in self.user_sessions.keys()):
            next_session = self.user_sessions[user_id] + 1
            if (next_session > MAX_SESSION):
                next_session -= MAX_SESSION
            
            self.user_sessions[user_id] = next_session
        else:
            self.user_sessions[user_id] = 1
        
        return self.user_sessions[user_id]
    

    # return current session value for a user
    def get_session(self, user_id):

        if (user_id in self.user_sessions.keys()):
            return self.user_sessions[user_id]
        else:
            self.user_sessions[user_id] = 1
        
        return 1

    
    # get binary data of last session
    def get_data(self, user_id):
        
        if (user_id in self.user_data.keys()):  
            return self.user_data[user_id]