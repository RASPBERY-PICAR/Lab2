# PC
import numpy as np
import cv2
import time
import threading
import socket
import struct
import io
from PIL import Image
import bluetooth

HOST = "172.20.10.3"  # IP address of your Raspberry PI
# HOST = "192.168.0.35"
PORT = 65432          # Port to listen on (non-privileged ports are > 1023)

sign = b'00'

#


def send_f():
    global sign
    host = "E4:5F:01:42:E0:84"
    port = 1
    sock = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
    sock.connect((host, port))
    while 1:
        # Note change to the old (Python 2) raw_input
        text = input("Enter your message: ")
        sock.send(text)
        print('sent', text, '\n')
        if (text == "quit"):
            sign = b'11'
            break
        # send the encoded message (send in binary format)
        if (text == "start"):
            sign = b'01'
        elif (text == "end"):
            sign = b'00'


def recv_st():
    global sign
    # stream_thread = threading.Thread(
    #     target=send_f, name='Thread', daemon=True)
    # stream_thread.start()

    # while 1:
    #     if sign == b'11':
    #         break
    #     elif sign == b'00':
    #         continue
    # need while
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
        client_socket.connect((HOST, PORT))
        connection = client_socket.makefile('rb')
        try:
            print("Streaming...Press 'q' to exit")
            while True:
                # Read the length of the image as a 32-bit unsigned int. If the
                # length is zero, quit the loop
                image_len = struct.unpack(
                    '<L', connection.read(struct.calcsize('<L')))[0]
                if not image_len:
                    # continue
                    break
                # Construct a stream to hold the image data and read the image
                # data from the connection
                image_stream = io.BytesIO()
                image_stream.write(connection.read(image_len))
                # Rewind the stream, open it as an image with PIL and do some
                # processing on it
                image_stream.seek(0)
                image = np.array(Image.open(image_stream))
                # b, g, r = cv2.split(image)
                # image = cv2.merge([r, g, b])
                cv2.imshow('image', image)
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break

        finally:
            # cv2.destroyAllWindows()
            connection.close()
            client_socket.close()


if __name__ == "__main__":
    recv_st()
