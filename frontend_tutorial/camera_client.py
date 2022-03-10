# PC
import numpy as np
import cv2
import time
import socket
import struct
import io
from PIL import Image

HOST = "172.20.10.3"  # IP address of your Raspberry PI
# HOST = "192.168.0.35"
PORT = 65432          # Port to listen on (non-privileged ports are > 1023)

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
    client_socket.connect((HOST, PORT))
    connection = client_socket.makefile('rb')
    start_sign = False
    try:
        print("Streaming...Press 'q' to exit")
        # need bytes here

        stream_bytes = b' '
        while True:
            # Read the length of the image as a 32-bit unsigned int. If the
            # length is zero, quit the loop
            image_len = struct.unpack(
                '<L', connection.read(struct.calcsize('<L')))[0]
            if not image_len:
                break
            # Construct a stream to hold the image data and read the image
            # data from the connection
            image_stream = io.BytesIO()
            image_stream.write(connection.read(image_len))
            # Rewind the stream, open it as an image with PIL and do some
            # processing on it
            image_stream.seek(0)
            image = Image.open(image_stream)
            stream_bytes += connection.read(1024)
            # stop = stream_bytes.find(b'\xff\xda')
            # if (stop == -1):
            #     break
            first = stream_bytes.find(b'\xff\xd8')
            last = stream_bytes.find(b'\xff\xd9')
            # print('first:', first, 'last:', last,
            #       'last-first:', last-first, '\n')
            if (first != -1 and last != -1):
                if not start_sign:
                    start_sign = True
                jpg = stream_bytes[first:last + 2]
                stream_bytes = stream_bytes[last + 2:]
                # image = cv2.imdecode(np.frombuffer(
                #     jpg, dtype=np.uint8), cv2.COLOR_RGB2BGR)
                image = cv2.imdecode(np.fromstring(
                    jpg, dtype=np.uint8), cv2.IMREAD_COLOR)
                # image = cv2.cvtColor(image, cv2.IMREAD_COLOR)
                cv2.imshow('image', image)
                if cv2.waitKey(30) & 0xFF == ord('q'):
                    print('q')

                    # time.sleep(0.5)
                    break
            else:
                if start_sign:
                    start_sign = False
                    print("end")
                    cv2.destroyAllWindows()
                    # time.sleep(0.5)
                    continue

    finally:
        # cv2.destroyAllWindows()
        connection.close()
        client_socket.close()
