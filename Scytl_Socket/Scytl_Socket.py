from functools import reduce
import MyConnection
import ProtocolX
import Util

def main():
    # Connection info
    port = 50029
    IP = '189.6.76.118'

    # Protocol info
    table1 = {'11110':	0x0, '01001':	0x1, '10100':	0x2, '10101':	0x3, '01010':	0x4, '01011':	0x5,\
       '01110':	0x6, '01111':	0x7, '10010':	0x8, '10011':	0x9, '10110':	0xA, '10111':	0xB, \
       '11010':	0xC, '11011':	0xD, '11100':	0xE, '11101':	0xF}

    protocol = ProtocolX.ProtocolX(table1)

    prime_factor = Util.get_prime_factor(port)

    # Connect
    connection = MyConnection.MyConnection(IP, port)

    recv_msg = connection.get_msg()
    print('recv_msg = ' + recv_msg)
    # Decode

    pkt_msg = Util.divide_packets(recv_msg)
    decoded_msg = ''
    for p in pkt_msg:
        decoded_msg += protocol.decode_packet(p)
    print('decoded_msg = ' + decoded_msg)
    # Process data
    processed_msg = Util.remove_space(decoded_msg)
    processed_msg = Util.upper_lower(processed_msg)
    processed_msg = processed_msg.replace(' ', '_')
    processed_msg = processed_msg[::-1] # invert message 

    print('Processed message: ' + processed_msg)

    # Encode
    while not len(processed_msg)%4:
        processed_msg += '_'

    lst = [processed_msg[i:i+4] for i in range(0, len(processed_msg), 4)]
    msg_to_send = ''
    for i in lst:
        encoded_msg = protocol.encode_packet(i)
        encoded_msg = map(lambda x : chr(x^prime_factor), Util.map_bin2int(encoded_msg))
        msg_to_send = chr(0xc6) + reduce(lambda a, b : a+b, encoded_msg, '') + chr(0x6b)
    msg_to_send = msg_to_send[:len(msg_to_send)-1] + chr(0x21)

    connection.send_msg(msg_to_send)

    # Confirmation
    msg_confirm = connection.get_msg()

    if msg_confirm == 'ÆWUzz\x9e!':
        print ("Well done!")
    elif msg_confirm == 'ÆR×EÒ\x9e!':
        print ("Error msg")
    else:
        print ("Big mistake")

    connection.close_socket()

if __name__ == '__main__':
    main()
