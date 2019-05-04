#! /usr/bin/python3

from threading import Lock


class GlobalData:

    sock = None
    lock = Lock()
    sequences = None
    sessions = None
    messages_ack = None
    nodes = None
    header = None


    @staticmethod
    def set_data(socket, sequences, sessions, messages_ack, nodes, header):
        GlobalData.sock = socket
        GlobalData.sequences = sequences
        GlobalData.sessions = sessions
        GlobalData.messages_ack = messages_ack
        GlobalData.nodes = nodes
        GlobalData.header = header