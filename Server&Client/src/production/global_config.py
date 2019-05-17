#! /usr/bin/python3

import yaml
from socket import gethostname


yaml_name = gethostname() + '.yaml'
conf = './config/' + yaml_name
yml = open(conf)
data =yaml.load(yml)

SERVER_KEY = data['server_key']
PROTOCOL_VERSION = 0

DEFAULT_DESTINATION = 'AC3C905F1239362C'

DEFAULT_SERVER_IP = data['server_ip']
DEFAULT_SERVER_PORT = data['server_port']

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

# send/request identity constants
ID_KEY = 'ID'
RESPONCE_KEY = 'responseRequired'
NAME_KEY = 'name'

# packet constants
packet_types = {
    'keepalive' : 0,
    'route_update' : 1,
    'full_table_request' : 2,
    'full_table_update' : 3,
    'send_request_identity' : 4,
    'group_message' : 5,
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

INIT_NODES = {
        SERVER_KEY: [DEFAULT_SERVER_IP, DEFAULT_SERVER_PORT, "self"],
        "ac3c905f1239362c": ["127.0.0.1", 8088, "t"]
}

RESEND_TIMEOUT_SEC = 5
KEEPALIVE_TIMER = 10
KEEPALIVE_LIMIT = 40

MAX_ROUTE_COST = 65535