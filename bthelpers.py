import bluetooth
import json
import struct

# target_name = "raspberrypi"
sock = None

# TODO: Implement server for p2p comms

def start_client():    
    host = "E4:5F:01:42:E0:84" # The address of Raspberry PI Bluetooth adapter on the server.
    port = 1
    sock = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
    sock.connect((host, port))
    # target_address = None
    # nearby_devices = bluetooth.discover_devices()

    # for bdaddr in nearby_devices:
    #     print(bluetooth.lookup_name( bdaddr ))
    #     if target_name == bluetooth.lookup_name( bdaddr ):
    #         target_address = bdaddr
    #         break

    # if target_address is not None:
    #     print ("found target bluetooth device with address ", target_address)
    # else:
    #     print ("could not find target bluetooth device nearby")

    # port = 1

    # sock=bluetooth.BluetoothSocket( bluetooth.RFCOMM )
    # sock.connect((target_address, port))      
def receive_data():
    data = sock.recv(1024)
    res = struct.unpack('%sf'%2, data)
    return res

def set_target(target):
    target_name = target

def send_data(data):
    print('using bthelpers function')
    print(data)
    sock.send(json.dumps(data))

def terminate():
    sock.close()


