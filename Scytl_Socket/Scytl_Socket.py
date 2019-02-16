import MyConnection

def main():
    # Connection info
    port = 50029
    IP = '189.6.76.118'

    # Connect
    connection = MyConnection.MyConnection(IP, port)

    recv_msg = connection.get_msg()

    # Decode

    # Process data

    # Encode


    # connection.send_msg(msg_to_send)
    # Confirmation
    # msg_confirm = connection.get_msg()

    connection.close_socket()

if __name__ == '__main__':
    main()
