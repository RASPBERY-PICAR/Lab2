import socket
import picar_4wd as picar
from time import sleep

HOST = "172.20.10.3" # IP address of your Raspberry PI
PORT = 65432          # Port to listen on (non-privileged ports are > 1023)
START = False

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen()
    
    try:
        while 1:
            client, clientInfo = s.accept()

            if not START:
                data = client.recv(1024)
                if data == b"Start":
                    START = True

            if START:
                sleep(0.05)
                status = picar.pi_read()
                battery_status = status['battery']
                cpu_temp = status['cpu_temperature']
                data = (str(battery_status) + ',' + str(cpu_temp)).encode('utf_8')
                client.send(data)
            
            # print("server recv from: ", clientInfo)
            # data = client.recv(1024)      # receive 1024 Bytes of message in binary format
            # if data != b"":
            #     print(data)     
            #     client.sendall(data) # Echo back to client
    except Exception as e: 
        print(e)
        print("Closing socket")
        client.close()
        s.close()    