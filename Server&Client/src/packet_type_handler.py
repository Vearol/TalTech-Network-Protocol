#! /usr/bin/python3

# 000   -- Keep alive
# 001   -- route update

# 010   -- Request full active routing table (Neighbor startup)
# 011   -- Full table route update

# 100   -- Send identity/request identity
# 101   -- N/A

# 110   -- Message, for screen
# 111   -- Message, binary with metadata

def keep_alive():
    print('keep alive message')
    # do something

def route_update():
    print('route update message')
    # do something

def full_table_request():
    print('request full active routing table message')
    # do something

def full_table_update():
    print('full table update message')
    # do something

def send_request_identity():
    print('sent/request identity message')
    # do something

def message_for_screen():
    print('message for screen')
    # do something

def message_with_metadata():
    print('message with binary metadata')
    # do something

def handle_packet_type(packet_type):
    if packet_type == 0:
        keep_alive()
        return

    if packet_type == 1:
        route_update()
        return

    if packet_type == 2:
        full_table_request()
        return

    if packet_type == 3:
        full_table_update()
        return

    if packet_type == 4:
        send_request_identity()
        return

    if packet_type == 6:
        message_for_screen()
        return

    if packet_type == 7:
        message_with_metadata()
        return

