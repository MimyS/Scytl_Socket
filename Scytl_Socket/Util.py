import re

def divide_packets(msg):
    tokens = '[' + chr(0xc6) + chr(0x6b) + chr(0x21) + ']'
    return list(filter(None, re.split(tokens, msg)))

def remove_space(msg):
    while msg[len(msg)-1] == ' ': #0x20 - space
        msg = msg[:len(msg)-1]
    return msg

