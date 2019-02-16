import MyConection
import ProtocolX
import Util

def main():
    # Connection info
    port = 50029
    IP = '189.6.76.118'

    # Connect
    connection = MyConnection.MyConnection(IP, port)

    recv_msg = connection.get_msg()

    # Decode
    protocol = ProtocolX.ProtocolX()
    decoded_msg = ''
    pkt_msg = Util.divide_packets(recv_msg)
    for p in pkt_msg:
        decoded_msg += protocol.decode_packet(p)

    # Process data
    processed_msg = Util.remove_space(dec_msg)

    # Encode
    #encoded_msg = ''
    #for i in range(len(processed_msg)-1,4,-4):
    #    encoded_msg += protocol.encode_packet(processed_msg[i-4:i])


    # connection.send_msg(msg_to_send)
    # Confirmation
    # msg_confirm = connection.get_msg()

    connection.close_socket()

if __name__ == '__main__':
    main()
