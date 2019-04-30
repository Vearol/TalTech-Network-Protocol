#! /usr/bin/python3

from colors import colors


def forward_message(sock, message, dest):
    
    #next_dest = get_next_dest(dest)

    print(colors.LOG, 'Forwarding massage to', dest)

    #sock.sendto(message, (next_dest.ip, next_dest.port))

