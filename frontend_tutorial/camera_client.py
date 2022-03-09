# PC
import numpy as np
import cv2
import time
import socket
import struct
# from PIL import Image

# HOST = "172.20.10.3"  # IP address of your Raspberry PI
HOST = "73.45.190.122"
PORT = 65432          # Port to listen on (non-privileged ports are > 1023)

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
    client_socket.connect((HOST, PORT))
    connection = client_socket.makefile('rb')
    start_sign = False
    try:
        print("Streaming...")
        print("Press 'q' to exit")
        # need bytes here
        stream_bytes = b' '
        while True:
            stream_bytes += connection.read(1024)
            # stop = stream_bytes.find(b'\xff\xda')
            # if (stop == -1):
            #     break
            first = stream_bytes.find(b'\xff\xd8')
            last = stream_bytes.find(b'\xff\xd9')
            if first != -1 and last != -1:
                print('first:', first, 'last:', last,
                      'last-first:', last-first, '\n')
                if not start_sign:
                    start_sign = True
                jpg = stream_bytes[first:last + 2]
                stream_bytes = stream_bytes[last + 2:]
                image = cv2.imdecode(np.frombuffer(
                    jpg, dtype=np.uint8), cv2.COLOR_RGB2BGR)
                # image = cv2.imdecode(np.frombuffer(
                #     jpg, dtype=np.uint8), cv2.IMREAD_COLOR)
                # image= cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
                cv2.imshow('image', image)
                if cv2.waitKey(1) & 0xFF == ord('q'):
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


# class VideoStreamingTest(object):
#     def __init__(self, host, port):

#         self.server_socket = socket.socket()
#         self.server_socket.bind((host, port))
#         self.server_socket.listen(0)
#         self.connection, self.client_address = self.server_socket.accept()
#         self.connection = self.connection.makefile('rb')
#         self.host_name = socket.gethostname()
#         self.host_ip = socket.gethostbyname(self.host_name)
#         self.streaming()

#     def streaming(self):

#         try:
#             print("Host: ", self.host_name + ' ' + self.host_ip)
#             print("Connection from: ", self.client_address)
#             print("Streaming...")
#             print("Press 'q' to exit")

#             # need bytes here
#             stream_bytes = b' '
#             while True:
#                 stream_bytes += self.connection.read(1024)
#                 first = stream_bytes.find(b'\xff\xd8')
#                 last = stream_bytes.find(b'\xff\xd9')
#                 if first != -1 and last != -1:
#                     jpg = stream_bytes[first:last + 2]
#                     stream_bytes = stream_bytes[last + 2:]
#                     image = cv2.imdecode(np.frombuffer(
#                         jpg, dtype=np.uint8), cv2.IMREAD_COLOR)
#                     cv2.imshow('image', image)
#                     if cv2.waitKey(1) & 0xFF == ord('q'):
#                         break
#         finally:
#             self.connection.close()
#             self.server_socket.close()


# if __name__ == '__main__':
#     # host, port
#     HOST = "172.20.10.3"  # IP address of your Raspberry PI
#     PORT = 65432          # Port to listen on (non-privileged ports are > 1023)
#     VideoStreamingTest(HOST, PORT)
