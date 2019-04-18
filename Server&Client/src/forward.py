#! /usr/bin/python3

def forward_message(sock, message, dest):
    
    next_dest = get_next_dest(dest)

    print('Forwarding massage to', next_dest.nickname)

    sock.sendto(message, (next_dest.ip, next_dest.port))

