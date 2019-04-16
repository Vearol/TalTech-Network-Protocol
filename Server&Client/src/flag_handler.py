#! /usr/bin/python3

from global_mapping import *

def normal():
    
    # do something


def first_packet():
   
    # do something


def last_packet():
    
    # do something


def single_packet():
   
    # do something


def ACK():
    
    # do something


def NOT_ACK():

    # Send ACK


def error():
    
    # do something


def handle_flag(socket, header, payload):
    
    flag = header.flag

    if flag == flag_types['normal']:
        normal()
        return

    if flag == flag_types['first_packet']:
        first_packet()
        return

    if flag == flag_types['last_packet']:
        last_packet()
        return

    if flag == flag_types['single_packet']:
        single_packet()
        return

    if flag == flag_types['ACK']:
        ACK()
        return

    if flag == flag_types['NOT_ACK']:
        NOT_ACK()
        return

    if flag == flag_types['error']:
        error()
        return

