import socket

HEADERSIZE = 10

hostMACAddress = '30:d3:7a:bf:bc:37' # The MAC address of a Bluetooth adapter on the server
port = 4
size = 1024
s = socket.socket(socket.AF_BLUETOOTH, socket.SOCK_STREAM, socket.BTPROTO_RFCOMM)
s.connect((hostMACAddress, port))

while True:
    full_msg= ''
    new_msg = True
    while True:
        msg = s.recv(16)
        if new_msg:
            msglen = int(msg[:HEADERSIZE])
            new_msg = False

        full_msg += msg.decode("utf-8")

        if len(full_msg)-HEADERSIZE == msglen:
            print(full_msg[HEADERSIZE:])
            new_msg = True
            full_msg = ''
    print(full_msg)
