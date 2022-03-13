# PC
import numpy as np
import cv2
# import time
# import threading
import socket
import struct
import io
from PIL import Image

HOST = "172.20.10.3"  # IP address of your Raspberry PI
PORT = 65432          # Port to listen on (non-privileged ports are > 1023)


# receive the video stream and display
# refer to https://picamera.readthedocs.io/en/release-1.13/recipes1.html#streaming-capture
def recv_st():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
        client_socket.connect((HOST, PORT))
        connection = client_socket.makefile('rb')
        try:
            print("Streaming...")
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
                b, g, r = cv2.split(image)
                image = cv2.merge([r, g, b])
                cv2.imshow('image', image)
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break

        finally:
            # cv2.destroyAllWindows()
            connection.close()
            client_socket.close()


if __name__ == "__main__":
    recv_st()
