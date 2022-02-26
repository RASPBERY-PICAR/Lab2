import bluetooth
import struct

host = "E4:5F:01:42:E0:84" # The address of Raspberry PI Bluetooth adapter on the server.
port = 1
sock = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
sock.connect((host, port))
while 1:
    text = input("Enter your message: ") # Note change to the old (Python 2) raw_input
    if text == "quit":
        break
    # sock.send(text)

    data = sock.recv(1024)
    res = struct.unpack('%sf' % 2, data)
    # print(type(data))
    print("from server: ", data)

sock.close()
