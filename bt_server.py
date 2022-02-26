import bluetooth
import picar_4wd as picar
from picar_4wd.utils import cpu_temperature, pi_read

status = pi_read()
battery_status = status['battery']
cpu_temp = status['cpu_temperature']

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
    # while 1:   
    #     print("server recv from: ", clientInfo)
    #     data = client.recv(size)
    #     if data:
    #         print(data)
    #         client.send(data) # Echo back to client
    client.send(battery_status, cpu_temp)
except: 
    print("Closing socket")
    client.close()
    s.close()

