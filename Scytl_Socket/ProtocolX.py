class ProtocolX(object):
    encode_table = ['11110', '01001', '10100', '10101', '01010', '01011', '01110', '01111', '10010', '10011', '10110', '10111', '11010', '11011', '11100', '11101']
    decode_table = {'11110':	0x0, '01001':	0x1, '10100':	0x2, '10101':	0x3, '01010':	0x4, '01011':	0x5, '01110':	0x6, '01111':	0x7, \
       '10010':	0x8, '10011':	0x9, '10110':	0xA, '10111':	0xB, '11010':	0xC, '11011':	0xD, '11100':	0xE, '11101':	0xF}

    def __init__(self):
        pass

    def decode_packet(self, msg): #um pacote apenas - len(msg) = 5
        value = int(reduce(lambda a,b: a+b, map_str2hex(msg)), 16)
        out_msg = ''
        for i in range(35,-1,-10):
            out_msg += chr( (self.decode_table['{:05b}'.format((value>>i)&0x1F)]<<4) \
                + self.decode_table['{:05b}'.format((value>>(i-5))&0x1F)])
        return out_msg

    def encode_packet(self, msg):
        value = int(reduce(lambda a,b: a+b, map_str2hex(msg)), 16)
        out_msg = ''
        for i in range(36,-1,-4):
            out_msg += self.encode_table[(value>>i)&0xF]
        return out_msg


def map_str2hex(msg):
    return list(map(lambda a : '{:02x}'.format(a), map(ord, msg)))

def map_char2int(msg):
    return map(ord, msg)

def map_int2bin(msg):
    return map(lambda x : '{:08b}'.format(x), msg)

def map_bin2int(msg):
    return map(lambda x : int(x,2), msg)

def map_int2char(msg):
    return map(chr, msg)

def break_msg(msg, n):
    return [msg[i:i+n] for i in range(0, len(msg), n)]