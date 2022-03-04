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
            print("Running")
            client, clientInfo = s.accept()
            data = client.recv(1024)

            if data == b"87\r\n": # up
                print('getting key info')
                print(data)
                picar.forward(20)
            if data == b"83\r\n": # down
                print('getting key info')
                print(data)
                picar.backward(20)
            if data == b"65\r\n": # left
                print('getting key info')
                print(data)
                picar.turn_left(90)
            if data == b"68\r\n": # right
                print('getting key info')
                print(data)
                picar.turn_right(90)

            if data == b"Exit\r\n":
                print('closing')
                client.close()
                s.close()
                break

            if not START:
                print("x")
                data = client.recv(1024)
                if data == b"Start\r\n":
                    START = True

            if START:
                sleep(1)
                status = picar.pi_read()
                battery_status = status['battery']
                cpu_temp = status['cpu_temperature']
                data2 = (str(battery_status) + ',' + str(cpu_temp)).encode('utf_8')
                print(battery_status,cpu_temp)
                print(data2)
                client.send(data2)
                # START = False
            # elif( data != b""):
            #     print(data)     
            #     #client.sendall(data) # Echo back to client
            #     print(START)
                
            
                          
             #print("server recv from: ", clientInfo)
             #data = client.recv(1024)      # receive 1024 Bytes of message in binary format
    except Exception as e: 
        print(e)
        print("Closing socket")
        client.close()
        s.close()    