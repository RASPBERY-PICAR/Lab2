import bluetooth
import os

# The address of Raspberry PI Bluetooth adapter on the server.
host = "E4:5F:01:42:E0:84"
port = 1
sock = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
sock.connect((host, port))
while 1:
    # Note change to the old (Python 2) raw_input
    text = input("Enter your message: ")
    sock.send(text)
    print('sent', text, '\n')
    if text == "quit":
        break
    elif (text == "start"):
        str = ('python3 camera_client.py')
        os.system(str)
    # elif (text == "end"):

    data = sock.recv(1024)
    print("recv from server: ", data, '\n')

sock.close()
