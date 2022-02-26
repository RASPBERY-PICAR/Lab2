import bluetooth
import picar_4wd as picar
import struct

status = picar.pi_read()
battery_status = status['battery']
cpu_temp = status['cpu_temperature']
res = [battery_status, cpu_temp]

hostMACAddress = "E4:5F:01:42:E0:84" # The address of Raspberry PI Bluetooth adapter on the server. The server might have multiple Bluetooth adapters.
port = 0
backlog = 1
size = 1024
s = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
s.bind((hostMACAddress, port))
s.listen(backlog)
print("listening on port ", port)
try:
    client, clientInfo = s.accept()
    while 1:   
        data = struct.pack('%sf' % len(res), *res)
        client.send(data)
        text = input("Enter to continue: ")
        # print("server recv from: ", clientInfo)
        # data = client.recv(size)
        # print('data type:', type(data))
        # if data:
        #     print(data)
        #     client.send(data) # Echo back to client
except Exception as e:
    print(e) 
    print("Closing socket")
    client.close()
    s.close()
