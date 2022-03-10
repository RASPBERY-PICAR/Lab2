# PC
import numpy as np
import cv2
import time
import socket
# from PIL import Image

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
                image = cv2.imdecode(np.frombuffer(
                    jpg, dtype=np.uint8), cv2.IMREAD_COLOR)
                image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
                cv2.imshow('image', image)
                if cv2.waitKey(30) & 0xFF == ord('q'):
                    cv2.destroyAllWindows()
                    time.sleep(0.5)
                    break
            else:
                if start_sign:
                    start_sign = False
                    print("end")
                    cv2.destroyAllWindows()
                    time.sleep(0.5)
                    continue

    finally:
        connection.close()
        client_socket.close()
