#! /usr/bin/python3

# 000   -- Keep alive
# 001   -- route update

# 010   -- Request full active routing table (Neighbor startup)
# 011   -- Full table route update

# 100   -- Send identity/request identity
# 101   -- N/A

# 110   -- Message, for screen
# 111   -- Message, binary with metadata

def keep_alive(payload):
    
    print('keep alive message')
    # do something


def route_update(payload):
   
    print('route update message')
    # do something


def full_table_request(payload):
    
    print('request full active routing table message')
    # do something


def full_table_update(payload):
   
    print('full table update message')
    # do something


def send_request_identity(payload):
    
    print('sent/request identity message')
    # do something


def message_for_screen(socket, header, payload):
    
    message_str = payload.decode('utf-8')

    source = header.source

    # TODO store in db
    print('message for screen from', source)
    print(message_str)

    # Send ACK


def message_with_metadata(payload):
    
    print('message with binary metadata')
    # do something


def handle_packet(socket, header, payload):
    
    packet_type = header.packet_type

    if packet_type == 0:
        keep_alive(payload)
        return

    if packet_type == 1:
        route_update(payload)
        return

    if packet_type == 2:
        full_table_request(payload)
        return

    if packet_type == 3:
        full_table_update(payload)
        return

    if packet_type == 4:
        send_request_identity(payload)
        return

    if packet_type == 6:
        message_for_screen(socket, header, payload)
        return

    if packet_type == 7:
        message_with_metadata(payload)
        return

