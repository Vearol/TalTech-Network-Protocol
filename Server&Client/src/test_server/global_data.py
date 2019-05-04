#! /usr/bin/python3

from threading import Lock


class GlobalData:

    sock = None
    lock = Lock()
    sequences = None
    sessions = None
    messages = None
    nodes = None
    header = None


    @staticmethod
    def set_data(socket, sequences, sessions, messages, nodes, header):
        GlobalData.sock = socket
        GlobalData.sequences = sequences
        GlobalData.sessions = sessions
        GlobalData.messages = messages
        GlobalData.nodes = nodes
        GlobalData.header = header