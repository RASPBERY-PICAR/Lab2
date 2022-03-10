# PC
import numpy as np
import cv2
import socket
import struct
# from PIL import Image

HOST = "172.20.10.3"  # IP address of your Raspberry PI
PORT = 65432          # Port to listen on (non-privileged ports are > 1023)

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
    client_socket.connect((HOST, PORT))
    connection = client_socket.makefile('rb')

    try:
        print("Streaming...")
        print("Press 'q' to exit")
        # need bytes here
        stream_bytes = b' '
        while True:
            stream_bytes += connection.read(1024)
            end = stream_bytes.find(b"end")
            if end != -1:
                break
            first = stream_bytes.find(b'\xff\xd8')
            last = stream_bytes.find(b'\xff\xd9')
            if first != -1 and last != -1:
                jpg = stream_bytes[first:last + 2]
                stream_bytes = stream_bytes[last + 2:]
                image1 = cv2.imdecode(np.frombuffer(
                    jpg, dtype=np.uint8), cv2.IMREAD_COLOR)
                image = cv2.cvtColor(image1, cv2.COLOR_RGB2BGR)
                cv2.imshow('image', image)
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break
    finally:
        connection.close()
        client_socket.close()
