#! /usr/bin/python3

class Header_Parser:
    def get_bits_value(self, number, bits):
        
        value = 0
        for i in range(bits):
            value |= number & (1 << i)

        return value


    def bytes_to_number(self, byte_array):
        
        value = 0
        size = len(byte_array)
        for i in range(size):
            byte = byte_array[size - 1 - i]
            for j in range(8):
                value |= (byte & (1 << j)) << (i * 8)
        return value


    def parse_flag(self, header_bytes, bits):
        
        self.flag = self.get_bits_value(header_bytes, bits)


    def parse_packet_type(self, header_bytes, bits):
        
        self.packet_type = self.get_bits_value(header_bytes, bits)


    def parse_protocol_version(self, header_bytes, bits):
        
        self.protocol_version = self.get_bits_value(header_bytes, bits)


    def parse_header(self, header_bytes):
        
        # byte 0        -- protocol version,packet type, flags
        byte0 = header_bytes[0]

        flag_bits = 3
        packet_type_bits = 3
        protocol_version_bits = 2

        self.parse_protocol_version(byte0, protocol_version_bits)
        byte0 = byte0 >> protocol_version_bits
        self.parse_packet_type(byte0, packet_type_bits)
        byte0 = byte0 >> packet_type_bits
        self.parse_flag(byte0, flag_bits)

        # byte 1..8     -- SRC ID
        byte1_8 = header_bytes[1:9]
        self.source = self.bytes_to_number(byte1_8)

        # byte 9..16    -- DST ID
        byte9_16 = header_bytes[9:17]
        self.destination = self.bytes_to_number(byte9_16)

        # byte 17       -- sessionID, identify flow between endpoints
        byte17 = header_bytes[17]
        self.session_Id = byte17

        # byte 18..19   -- sequence number
        byte18_19 = header_bytes[18:20]
        self.sequence_number = self.bytes_to_number(byte18_19)
