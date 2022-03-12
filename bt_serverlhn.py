import bluetooth
import socket
import picar_4wd as picar
from time import sleep
import helper_functions as hf

hostMACAddress = "E4:5F:01:42:E0:84" # The address of Raspberry PI Bluetooth adapter on the server. The server might have multiple Bluetooth adapters.
port = 1
backlog = 1
size = 1024
s = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
s.bind((hostMACAddress, port))
s.listen(backlog)
print("listening on port ", port)
try:
        print("listen")
        client, clientInfo = s.accept()
        data = client.recv(1024)
        
        while 1:
            print("Running")
            
            
            
            print(data)

            if data == b"Begin\r\n":
                #sleep(1)
                status = picar.pi_read()
                battery_status = (status['battery']-6)/2*100
                cpu_temp = status['cpu_temperature']
                data2 = (str(battery_status)+"%"+ ',' + str(cpu_temp)+" C").encode('utf_8')
                print(battery_status,cpu_temp)
                #data2 = ('1,2').encode('utf_8')
                print(data2)
                client.send(data2)
            else:
                data3 = (' , ').encode('utf_8')
                client.send(data3)
            sleep(1)
except: 
    print("Closing socket")
    client.close()
    s.close()

