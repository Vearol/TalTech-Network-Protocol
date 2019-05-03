#! /usr/bin/python3

from byte_parser import set_bits, number_to_bytes, GPG_to_bytes
from global_config import HEADER_BUFFER


def create_header(protocol_version, packet_type, flag, source, destination, sessionId, sequence_number):
    
    header = bytearray(HEADER_BUFFER)
    #byte 0        -- protocol version,packet type, flags
    #bits 0..1 -- protocol version  Currently always Version 0x00
    #bits 2..4 -- packet type
    #bits 5..7 -- flags

    byte0 = set_bits(0, 0, 1, protocol_version)
    byte0 = set_bits(byte0, 2, 4, packet_type)
    byte0 = set_bits(byte0, 5, 7, flag)
    
    header[0] = byte0

    #byte 1..8     -- SRC ID
    header[1:9] = GPG_to_bytes(source)

    #byte 9..16    -- DST ID
    header[9:17] = GPG_to_bytes(destination)

    #byte 17       -- sessionID, identify flow between endpoints
    header[17] = sessionId

    #byte 18..19   -- sequence number
    header[18:20] = number_to_bytes(sequence_number, 2)

    return header


def create_packet(protocol_version, packet_type, flag, source, destination, sessionId, sequence_number, payload):
    
    packet = bytearray(HEADER_BUFFER + 1)

    packet[0:HEADER_BUFFER] = create_header(protocol_version, packet_type, flag, source, destination, sessionId, sequence_number)
    packet[HEADER_BUFFER:] = payload

    return packet