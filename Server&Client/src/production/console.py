#! /usr/bin/python3

import time
from colors import colors
from message import Message
from global_config import packet_types
from global_data import GlobalData


class Console:

    def __init__(self):
        self.MENU_PROMPT = 'Menu:\n' + \
                           '1. send message\n' + \
                           '2. send file\n' + \
                           '3. show contact list\n' + \
                           ': '
        self.MSG_PROMPT = 'Enter message: '
        self.FILE_PROMPT = 'Enter file path: '
        self.DEST_PROMPT = 'Enter destination id: '
        self.ERROR_MSG = 'The input is invalid.\n'

    def start(self):
        while True:
            time.sleep(0.5)
            mode = input(self.create_msg(self.MENU_PROMPT))

            if mode == '1':
                dest = input(self.create_msg(self.DEST_PROMPT))
                message = input(self.create_msg(self.MSG_PROMPT))
                Message.send_message(packet_types['screen_message'],
                                     dest,
                                     message.encode())
                continue

            if mode == '2':
                dest = input(self.create_msg(self.DEST_PROMPT))
                file_path = input(self.create_msg(self.FILE_PROMPT))
                Message.send_file(dest, file_path)
                continue

            if mode == '3':
                nodes_data = GlobalData.nodes.nodes_data
                count = 1
                for key, value in nodes_data.items():
                    nickname = value[2]
                    msg = str(count) + "." + nickname + ":\t" + key
                    print(self.create_msg(msg))
                print('\n')
                continue

            else:
                print(self.create_msg(self.ERROR_MSG))

    def create_msg(self, prompt):
        return colors.INPUT + prompt + colors.TEXT
