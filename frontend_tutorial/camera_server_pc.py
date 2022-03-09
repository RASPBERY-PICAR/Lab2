# pi
from ctypes import sizeof
import io
import socket
import struct
import time
from PIL import Image
import threading
import numpy as np
import cv2

# HOST = "172.20.10.3"  # IP address of your Raspberry PI
HOST = "192.168.0.35"
PORT = 65432          # The port used by the server


# server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# server_socket.bind((HOST, PORT))
# server_socket.listen(0)
# client, clientInfo = server_socket.accept()
# connection = client.makefile('wb')
# stop_sign = False


def pc_streaming():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((HOST, PORT))
    server_socket.listen(0)
    client, clientInfo = server_socket.accept()
    connection = client.makefile('wb')
    stop_sign = False

    # global server_socket, stop_sign
    # connection = client.makefile('wb')
    #
    camera = cv2.VideoCapture(0)
    print(camera)
    # start = time.time()
    while 1:
        # if stop_sign:
        #     break
        success, image = camera.read()
        cv2.imshow('frame', image)
        k = cv2.waitKey(30) & 0xff
        if k == ord('q'):
            break
        r, buf = cv2.imencode(".jpg", image)
        bytes_image = Image.fromarray(np.uint8(buf)).tobytes()
        detect_face_image = io.BytesIO(bytes_image)
        print(detect_face_image.getvalue())
        size = detect_face_image.tell()
        # print(size, 'x')
        if 1:
            connection.write(b'\xff\xd8')
            connection.write(struct.pack('<L', size))
            connection.flush()  # write data in buffer into file, clean buffer
            detect_face_image.seek(0)  # return to index 0
            connection.write(detect_face_image.read(size))
            connection.write(b'\xff\xd9')

        # Write the terminating 0-length to the connection to let the
        # server know we're done
        connection.write(struct.pack('<L', 0))
        # finish = time.time()
    cv2.destroyAllWindows()
    camera.release()
    # connection.write(b'\xff\xda')
    connection.close()


def main():
    global server_socket, client, connection, stop_sign
    stop_cnt = 0
    while (stop_cnt < 2):
        time.sleep(0.1)
        print(1)
        data = client.recv(1024)
        # print(data)
        if data == b'start':
            print(data)
            stop_sign = False
            connection = client.makefile('wb')
            stream_thread = threading.Thread(
                target=pc_streaming, name='Thread', daemon=True)
            stream_thread.start()
        elif data == b"end":
            # print(data)
            stop_cnt += 1
            stop_sign = True
            continue

    # print(stream_thread.name+' is alive ', stream_thread.isAlive())

    return


if __name__ == "__main__":
    pc_streaming()


# import io
# import socket
# import struct
# import time
# import picamera
# server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# server_socket.bind((HOST, PORT))
# server_socket.listen(0)
# connection = server_socket.accept()[0].makefile('wb')

# try:
#     with picamera.PiCamera() as camera:
#         camera.resolution = (320, 240)      # pi camera resolution
#         camera.framerate = 15               # 15 frames/sec
#         # give 2 secs for camera to initilize
#         time.sleep(2)
#         start = time.time()
#         stream = io.BytesIO()

#         # send jpeg format video stream
#         for foo in camera.capture_continuous(stream, 'jpeg', use_video_port=True):
#             connection.write(struct.pack('<L', stream.tell()))
#             connection.flush()
#             stream.seek(0)
#             connection.write(stream.read())
#             if time.time() - start > 600:
#                 break
#             stream.seek(0)
#             stream.truncate()
#     connection.write(struct.pack('<L', 0))
# finally:
#     connection.close()
#     server_socket.close()
