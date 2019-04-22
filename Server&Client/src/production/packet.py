#! /usr/bin/python3

def set_bits(number, bit_from, bit_to, value):

    k = 0
    bit_to += 1
    for i in range(bit_from, bit_to):
        number |= (value & (1 << k)) << bit_from
        k += 1
    
    return number


def number_to_bytes(value, size):

    byte_arr = bytearray(size)
    for i in range(size):
        for j in range(8):
            byte_arr[size - 1 - i] |= value & (1 << j)
        
        value = value >> 8
    
    return byte_arr


def create_header(protocol_version, packet_type, flag, source, destination, sessionId, sequence_number):
    
    header = bytearray(20)
    #byte 0        -- protocol version,packet type, flags
    #bits 0..1 -- protocol version  Currently always Version 0x00
    #bits 2..4 -- packet type
    #bits 5..7 -- flags

    byte0 = set_bits(0, 0, 1, protocol_version)
    byte0 = set_bits(byte0, 2, 4, packet_type)
    byte0 = set_bits(byte0, 5, 7, flag)
    
    header[0] = byte0

    #byte 1..8     -- SRC ID
    header[1:9] = number_to_bytes(source, 8)

    #byte 9..16    -- DST ID
    header[9:17] = number_to_bytes(destination, 8)

    #byte 17       -- sessionID, identify flow between endpoints
    header[17] = sessionId

    #byte 18..19   -- sequence number
    header[18:20] = number_to_bytes(sequence_number, 2)

    return header


def create_packet(protocol_version, packet_type, flag, source, destination, sessionId, sequence_number, payload):
    
    packet = bytearray(21)

    packet[0:20] = create_header(protocol_version, packet_type, flag, source, destination, sessionId, sequence_number)
    packet[20:] = payload

    return packet