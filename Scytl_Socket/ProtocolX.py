from functools import reduce

class ProtocolX(object):
    def __init__(self, table):
        aux_table = [(i+j,(m<<4)+n) for (i,m) in table.items() for (j,n) in table.items()]
        self.encode_table = [i for (i,j) in aux_table]
        self.decode_table = dict(aux_table)

    def decode_packet(self, msg): # len(msg) = 5
        pt1 = chr(self.decode_table['{:010b}'.format(  (ord(msg[0])       <<2)|(ord(msg[1])>>6))])
        pt2 = chr(self.decode_table['{:010b}'.format( ((ord(msg[1]) &0x3F)<<4)|(ord(msg[2])>>4))])
        pt3 = chr(self.decode_table['{:010b}'.format( ((ord(msg[2]) &0x0F)<<6)|(ord(msg[3])>>2))])
        pt4 = chr(self.decode_table['{:010b}'.format( ((ord(msg[3]) &0x03)<<8)|ord(msg[4]))])
        return pt1+pt2+pt3+pt4

    def encode_packet(self, msg):
        return reduce(lambda a, b : a+b, map(lambda x : self.encode_table[ord(x)], msg), '')