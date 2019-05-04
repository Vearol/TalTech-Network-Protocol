#! /usr/bin/python3

SERVER_KEY = 'F0DC905F05793A3C'
PROTOCOL_VERSION = 0

DEFAULT_DESTINATION = 'AC3C905F1239362C'

DEFAULT_SERVER_IP = '127.0.0.1'
DEFAULT_SERVER_PORT = 8080

DEFAULT_DEST_IP = '127.0.0.1'
DEFAULT_DEST_PORT = 8088

HEADER_BUFFER = 20
PAYLOAD_BUFFER = 80

# maximum sequence number 
MAX_SN = 65535
MAX_SESSION = 255

# metadata constants
METADATA_HEADER = 2
FILENAME_KEY = 'name'
FILESIZE_KEY = 'length'
FILETYPE_KEY = 'content-type'

# packet constants
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

INIT_NEIGHBORS = {
        "nodeself": ["127.0.0.1", 8088]
}