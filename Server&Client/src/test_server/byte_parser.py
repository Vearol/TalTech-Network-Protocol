#! /usr/bin/python3

# get value of first N bits in number
def get_bits(number, bits):
        
    value = 0
    for i in range(bits):
        value |= number & (1 << i)

    return value


# set bits in a number in position (from-to) to the value
def set_bits(number, bit_from, bit_to, value):

    k = 0
    bit_to += 1
    for i in range(bit_from, bit_to):
        number |= (value & (1 << k)) << bit_from
        k += 1
    
    return number


# convert bytearray to number
def bytes_to_number(byte_array):
        
    value = 0
    size = len(byte_array)
    for i in range(size):
        byte = byte_array[size - 1 - i]
        for j in range(8):
            value |= (byte & (1 << j)) << (i * 8)
    return value


# convert number to bytearray of given size
def number_to_bytes(value, size):

    byte_arr = bytearray(size)
    for i in range(size):
        for j in range(8):
            byte_arr[size - 1 - i] |= value & (1 << j)
        
        value = value >> 8
    
    return byte_arr