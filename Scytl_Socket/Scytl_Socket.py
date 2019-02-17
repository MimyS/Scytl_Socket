from functools import reduce
import MyConnection
import ProtocolX
import Util
import sys

def main():
    nxt_port = False
    default_port = True
    nxt_ip = False
    default_ip = True
    for i in sys.argv:
        if i.lower() == '-h':
            print("\n~~~~//~~~~//~~~~//~~~~//~~~~//~~~~//~~~~//~~~~//~~~~//~~~~//~~~~//~~~//~~~~//~~~~//~~~~//~~~~//~~~~//~~~~//~~~~\n")
            print("Socket Development Test by Emily Souza")
            print("\nThe program was developed using python 3.7 and do NOT work with versions older than 3.6")
            print("\nCommands:\n")
            print("-p,  change the port number (default 50029)")
            print("-a,  change the IP address (default '189.6.76.118')")
            print("-h,  display this help text and exit (ignoring others setting options)")
            print("-i,  display the program introduction right before running")
            print("\nMore informations avaliable (in portuguese) at the README file")
            print("\n~~~~//~~~~//~~~~//~~~~//~~~~//~~~~//~~~~//~~~~//~~~~//~~~~//~~~~//~~~//~~~~//~~~~//~~~~//~~~~//~~~~//~~~~//~~~~\n")
            return
        elif nxt_port:
            port = int(i)
            nxt_port = False
            default_port = False
        elif nxt_ip:
            ip = i
            nxt_ip = False
            default_ip = False
        elif i.lower() == '-p':
            nxt_port = True
        elif i.lower() == '-a':
            nxt_ip = True
        elif i.lower() == '-i':
            print("\n~~~~//~~~~//~~~~//~~~~//~~~~//~~~~//~~~~//~~~~//~~~~//~~~~//~~~~//~~~//~~~~//~~~~//~~~~//~~~~//~~~~//~~~~//~~~~\n")
            print("Socket Development Test for the internship selection process of Scytl - Innovating Democracy.")
            print("Developer: Emily Souza\n")
            print("The program was developed using python 3.7 and do NOT work with versions older than 3.6\n")
            print("The main functionalities are:")
            print("1) Connecting to Scytl's Server using the IP Address '189.6.76.118' and port 50029")
            print("2) Receiving packets from de server encoded using \"Protocol X\"")
            print("3) Decoding the message to obtain the original one")
            print("4) Changing spaces to underlines and strings to lower and upper characters")
            print("5) Inverting the message")
            print("6) Reencoding the message with the same protocol")
            print("7) Sending the resulting data back to the server")
            print("8) Getting a confirmation from the server")
            print("\n~~~~//~~~~//~~~~//~~~~//~~~~//~~~~//~~~~//~~~~//~~~~//~~~~//~~~~//~~~//~~~~//~~~~//~~~~//~~~~//~~~~//~~~~//~~~~\n")
            print("Running the program...\n")

    # Connection info
    if default_port:
        port = 50029
    if default_ip:
        IP = '189.6.76.118'

    # Protocol info
    table1 = {'11110':	0x0, '01001':	0x1, '10100':	0x2, '10101':	0x3, '01010':	0x4, '01011':	0x5,\
       '01110':	0x6, '01111':	0x7, '10010':	0x8, '10011':	0x9, '10110':	0xA, '10111':	0xB, \
       '11010':	0xC, '11011':	0xD, '11100':	0xE, '11101':	0xF}

    protocol = ProtocolX.ProtocolX(table1)

    prime_factor = Util.get_prime_factor(port)

    # Open Connection
    connection = MyConnection.MyConnection(IP, port)

    recv_msg = connection.get_msg()

    # Decode
    pkt_msg = Util.divide_packets(recv_msg)
    decoded_msg = ''
    for p in pkt_msg:
        decoded_msg += protocol.decode_packet(p)

    # Process data
    processed_msg = Util.remove_space(decoded_msg)
    print("Decoded message: " + processed_msg + '\n')

    processed_msg = Util.upper_lower(processed_msg)
    processed_msg = processed_msg.replace(' ', '_')
    processed_msg = processed_msg[::-1] # invert message 

    print("Processed message: " + processed_msg + '\n')

    # Encode
    while len(processed_msg)%4:
        processed_msg += '_'

    lst = [processed_msg[i:i+4] for i in range(0, len(processed_msg), 4)]
    msg_to_send = ''
    for i in lst:
        encoded_msg = protocol.encode_packet(i)
        encoded_msg = [int(encoded_msg[x:x+8],2) for x in range(0,len(encoded_msg),8)]
        encoded_msg = list(map(lambda x:x^prime_factor, encoded_msg))
        msg_to_send += chr(0xc6) + reduce(lambda a, b : a+chr(b), encoded_msg, '') + chr(0x6b)
    msg_to_send = msg_to_send[:len(msg_to_send)-1] + chr(0x21)

    connection.send_msg(msg_to_send)
    print("Sent message: " + reduce(lambda x, y : x+' '+hex(ord(y)), msg_to_send, '') + '\n')

    # Confirmation
    msg_confirm = connection.get_msg()
    pkt_msg = Util.divide_packets(msg_confirm)

    msg_confirm = ''
    for p in pkt_msg:
        msg_confirm += protocol.decode_packet(p)
    msg_confirm = Util.remove_space(msg_confirm)

    print ("Confirmation message: " + msg_confirm + '\n')

    # Close Connection
    connection.close_socket()

if __name__ == '__main__':
    main()
