# pi
import io
import socket
import struct
import time
import picamera


class SplitFrames(object):
    def __init__(self, connection):
        self.connection = connection
        self.stream = io.BytesIO()
        self.count = 0

    def write(self, buf):
        if buf.startswith(b'\xff\xd8'):
            # Start of new frame; send the old one's length
            # then the data
            size = self.stream.tell()
            if size > 0:
                self.connection.write(struct.pack('<L', size))
                self.connection.flush()
                self.stream.seek(0)
                self.connection.write(self.stream.read(size))
                self.count += 1
                self.stream.seek(0)
        self.stream.write(buf)


HOST = "172.20.10.3"  # IP address of your Raspberry PI
PORT = 65432          # The port used by the server

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((HOST, PORT))
server_socket.listen(0)
connection = server_socket.accept()[0].makefile('wb')
try:
    output = SplitFrames(connection)
    with picamera.PiCamera(resolution='VGA', framerate=30) as camera:
        time.sleep(2)
        i = 3
        while i:
            i = i-1
            start = time.time()
            camera.start_recording(output, format='mjpeg')
            camera.wait_recording(10)
            camera.stop_recording()
            # Write the terminating 0-length to the connection to let the
            # server know we're done
            connection.write(struct.pack('<L', 0))
            finish = time.time()
            print('Sent %d images in %d seconds at %.2ffps' % (
                output.count, finish-start, output.count / (finish-start)))
finally:
    connection.close()
    server_socket.close()


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
