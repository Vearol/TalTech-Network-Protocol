#! /usr/bin/python3

import os
import json

from byte_parser import bytes_to_number
from global_mapping import METADATA_HEADER, FILENAME_KEY, FILESIZE_KEY, FILETYPE_KEY


def generate_file_metadata(file_path):
    
    name = os.path.basename(file_path)
    size = os.path.getsize(file_path)
    content = name.split('.')[-1]

    metadata = {}

    metadata[FILENAME_KEY] = name
    metadata[FILESIZE_KEY] = size
    metadata[FILETYPE_KEY] = content

    metadata_json = json.dumps(metadata)
    metadata_bytes = metadata_json.encode()

    return (metadata_bytes, size)


def parse_file_metadata(payload):

    metadata_size = bytes_to_number(payload[0 : METADATA_HEADER])

    if (metadata_size != 0):
        
        metadata_str = payload[METADATA_HEADER : METADATA_HEADER + metadata_size].decode()
        metadata_dict = json.loads(metadata_str)

        return (metadata_dict, METADATA_HEADER + metadata_size)
    
    return ({}, 0)



