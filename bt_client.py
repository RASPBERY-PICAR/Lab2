import bluetooth
from picar_4wd.utils import pi_read

status = pi_read()
battery_status = status['battery']
cpu_temp = status['cpu_temperature']

host = "9C:B6:D0:F1:D7:DC" # The address of Raspberry PI Bluetooth adapter on the server.
port = 1
sock = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
sock.connect((host, port))
while 1:
    # text = input("Enter your message: ") # Note change to the old (Python 2) raw_input
    # if text == "quit":
    #     break
    sock.send(battery_status)
    sock.send(cpu_temp)


    # data = sock.recv(1024)
    # print("from server: ", data)

sock.close()


