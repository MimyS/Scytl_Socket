import re

def divide_packets(msg):
    tokens = '[' + chr(0xc6) + chr(0x6b) + chr(0x21) + ']'
    return list(filter(None, re.split(tokens, msg)))

def remove_space(msg):
    while msg[len(msg)-1] == ' ': #0x20 - space
        msg = msg[:len(msg)-1]
    return msg

def upper_lower(msg):
    length = len(msg)
    out_msg = ''
    for i in range(0, length-1, 2):
        out_msg += msg[i].upper() + msg[i+1].lower() # even2upper - odd2lower - 0 is even
    if length%2: # if even to upper last char
        out_msg += msg[length-1].upper()
    return out_msg

def get_prime_factor(port):
    value = 1
    factor = 2
    while port > 1:
        count = 0
        while not port%factor:
            count += 1
            port /= factor
        if count and factor < 255:
            value = factor
        factor += 1
    return value
