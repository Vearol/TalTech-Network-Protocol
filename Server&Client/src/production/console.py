#! /usr/bin/python3

import time
import pprint
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
                           '4. show current routing data\n' + \
                           '5. show appropriate neighbor of given dest\n' + \
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
                dest_nickname = input(self.create_msg(self.DEST_PROMPT))
                message = input(self.create_msg(self.MSG_PROMPT))
                dect_key = GlobalData.nodes.get_key_by_nickname(dest_nickname)
                if (dect_key == None): 
                    print(colors.ERROR, "No such node in contacts")
                    continue
                neighbor_id = GlobalData.nodes.get_nearest_neighbor(dect_key)
                Message.send_message(packet_types['screen_message'],
                                     neighbor_id,
                                     message.encode())
                continue

            if mode == '2':
                dest_nickname = input(self.create_msg(self.DEST_PROMPT))
                dect_key = GlobalData.nodes.get_key_by_nickname(dest_nickname)
                if (dect_key == None): 
                    print(colors.ERROR, "No such node in contacts")
                    continue
                neighbor_id = GlobalData.nodes.get_nearest_neighbor(dect_key)
                file_path = input(self.create_msg(self.FILE_PROMPT))
                Message.send_file(neighbor_id, file_path)
                continue

            if mode == '3':
                nodes_data = GlobalData.nodes.nodes_data
                cnt = 1
                for key, value in nodes_data.items():
                    ip = value[0]
                    if not ip:
                        ip = "Non-neighbor node"
                    nickname = value[2]
                    msg = str(cnt) + ". " + nickname + ":\t" + key + "\t" + ip
                    print(self.create_msg(msg))
                print('\n')
                continue

            if mode == '4':
                tables = GlobalData.nodes.tables
                pp = pprint.PrettyPrinter(indent=4)
                pp.pprint(tables)
                print('\n')
                continue

            if mode == '5':
                dest_nickname = input(self.create_msg(self.DEST_PROMPT))
                dect_key = GlobalData.nodes.get_key_by_nickname(dest_nickname)
                if (dect_key == None): 
                    print(colors.ERROR, "No such node in contacts")
                    continue

                neighbor_id = GlobalData.nodes.get_nearest_neighbor(dect_key)
                if not neighbor_id:
                    print(self.create_msg('No appropriate neighbor.'))
                else:
                    msg = "Forward to {}".format(neighbor_id)
                    print(self.create_msg(msg))
                print('\n')
                continue

            else:
                print(self.create_msg(self.ERROR_MSG))

    def create_msg(self, prompt):
        return colors.INPUT + prompt + colors.TEXT
