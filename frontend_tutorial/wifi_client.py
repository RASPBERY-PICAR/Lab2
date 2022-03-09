import socket

HOST = "192.168.0.35"  # IP address of your Raspberry PI
PORT = 52527          # Port to listen on (non-privileged ports are > 1023)

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    while 1:
        # Note change to the old (Python 2) raw_input
        text = input("Enter your message: ")
        if text == "quit":
            break
        # send the encoded message (send in binary format)
        s.send(text.encode())

        data = s.recv(1024)
        print("from server: ", data)
