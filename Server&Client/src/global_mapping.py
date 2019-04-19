#! /usr/bin/python3

SERVER_KEY = '...'
PROTOCOL_VERSION = 0

packet_types = {
    'keepalive' : 0,
    'route_update' : 1,
    'full_table_request' : 2,
    'full_table_update' : 3,
    'send_request_identity' : 4,
    'screen_message' : 6,
    'metadata_message' : 7
}

flag_types = {
    'normal' : 0,
    'first_packet' : 1,
    'last_packet' : 2,
    'single_packet' : 3,
    'ACK' : 4,
    'NOT_ACK' : 6,
    'error' : 7
}