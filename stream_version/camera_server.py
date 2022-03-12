# pi
import io
import socket
import struct
import time
import picamera
import threading
import bluetooth
import picar_4wd as picar
import helper_functions as hf
# wifi
HOST = "172.20.10.3"  # IP address of your Raspberry PI
PORT = 65432          # The port used by the server

# bluetooth
# The address of Raspberry PI Bluetooth adapter on the server. The server might have multiple Bluetooth adapters.
hostMACAddress = "E4:5F:01:42:E0:84"
port = 1
backlog = 1
size = 1024


stop_sign = False


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
                self.connection.flush()  # write data in buffer into file, clean buffer
                self.stream.seek(0)  # return to index 0
                self.connection.write(self.stream.read(size))  # send old frame
                self.count += 1
                self.stream.seek(0)  # return to index 0
        self.stream.write(buf)  # store new frame


def streaming():
    global stop_sign
    # connection = client.makefile('wb')
    #
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((HOST, PORT))
    server_socket.listen(0)
    client, clientInfo = server_socket.accept()
    print("server recv from: ", clientInfo)
    connection = client.makefile('wb')
    output = SplitFrames(connection)
    try:
        output = SplitFrames(connection)
        with picamera.PiCamera(resolution='VGA', framerate=30) as camera:
            time.sleep(2)
            start = time.time()
            while True:
                if stop_sign:
                    break
                camera.start_recording(output, format='mjpeg')
                camera.wait_recording(10)
                camera.stop_recording()
                # Write the terminating 0-length to the connection to let the
                # server know we're done

    finally:
        connection.write(struct.pack('<L', 0))
        connection.close()
        client.close()
        server_socket.close()
        finish = time.time()
        print('Sent %d images in %d seconds at %.2ffps' % (
            output.count, finish-start, output.count / (finish-start)))


def main():
    global stop_sign

    server_bt = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
    server_bt.bind((hostMACAddress, port))
    server_bt.listen(backlog)
    print("listening on port ", port)
    try:
        client_bt, client_bt_Info = server_bt.accept()
        while 1:
            print("server recv from: ", client_bt_Info)
            data = client_bt.recv(size)
            if data:
                print('get data: ', data, '\n')
                # client_bt.send(data)  # Echo back to client
            if data == b"87\r\n":  # up
                # hf.forward_grid()
                picar.forward(20)
            elif data == b"83\r\n":  # down
                # hf.backward_grid()
                picar.backward(20)
            elif data == b"65\r\n":  # left
                hf.turn_left_deg()
            elif data == b"68\r\n":  # right
                hf.turn_right_deg()
            elif data == b"polling\r\n":
                status = picar.pi_read()
                battery_status = (status['battery']-6)/2*100
                cpu_temp = status['cpu_temperature']
                data = (str(battery_status)+"%" + ',' +
                        str(cpu_temp)+" C").encode('utf_8')
                print(data)
                client_bt.send(data)
            elif data == b"stm_st\r\n":
                stop_sign = False
                stream_thread = threading.Thread(
                    target=streaming, name='Thread', daemon=True)
                stream_thread.start()
            elif data == b"stm_ed\r\n":
                stop_sign = True
                continue
            elif data == b"quit\r\n":
                stop_sign = True
                break
            else:
                picar.stop()
    except:
        print("Closing socket")
        client_bt.close()
        server_bt.close()

    # stop_cnt = 0
    # while (stop_cnt < 2):
    #     data = client.recv(1024)
    #     if data == b"start\r\n":
    #         print(data)
    #         stop_sign = False
    #         connection = client.makefile('wb')
    #         stream_thread = threading.Thread(
    #             target=streaming, name='Thread', daemon=True)
    #         stream_thread.start()
    #     elif data == b"end\r\n":
    #         stop_cnt += 1
    #         stop_sign = True
    #         break

    # print(stream_thread.name+' is alive ', stream_thread.isAlive())

    return


if __name__ == "__main__":

    main()
