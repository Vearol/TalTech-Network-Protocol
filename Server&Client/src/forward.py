#! /usr/bin/python3

def forward_message(socket, message, dest):
    
    next_dest = get_next_dest(dest)

    print('Forwarding massage to', next_dest.nickname)

    s.sendto(message, (next_dest.ip, next_dest.port))

