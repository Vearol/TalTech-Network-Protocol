#! /usr/bin/python3

def create_header(protocol_version, packet_type, flags, source, destination, sessionId, sequence_number):
    
    header = bytearray(20)
    


def create(protocol_version, packet_type, flags, source, destination, sessionId, sequence_number, payload):
    
    header = create_header(protocol_version, packet_type, flags, source, destination, sessionId, sequence_number)

