# import the library
import can
import time

class Device:
    def __init__(self, name, id, status="off"):
        self.name = name
        self.id = id
        self.status = status

    def __str__(self):
        return f"Urządzenie: {self.name},\t ID: {self.id},\t Status: {self.status}"

def getHeartbeatSnd(id):
    msg = can.Message(arbitration_id=id, is_extended_id=True, is_fd=True, data=[0x00, 0x00, 0x00])
    return msg

def getHeartbeatRcv(id):
    msg = can.Message(arbitration_id=id, is_extended_id=True, is_fd=True, data=[0x00, 0x00, 0x00])
    return msg

devices = [
    Device("Nawigacja", 101),
    Device("Bateria1", 102),
    Device("ModEx90", 103)
]


def switchOn(id):
    dev=next((device for device in devices if device.id == id), None)
    if(dev!=None):
        dev.status="ON"
    else:
        print("Nie ma urządzenia o id: ", id)


def switchOff(id):
    dev=next((device for device in devices if device.id == id), None)
    if(dev!=None):
        dev.status="OFF"
    else:
        print("Nie ma urządzenia o id: ", id)

def switchToggle(id):
    dev=next((device for device in devices if device.id == id), None)
    if(dev!=None):
        if(dev.status=="on"):
            dev.status="off"
        elif(dev.status=="off"):
            dev.status="on"
    else:
        print("Nie ma urządzenia o id: ", id)





bus=can.Bus(interface='socketcan', channel='vcan0', fd=True) 
# notifier = can.Notifier(bus, [can.Logger("recorded.log"), can.Printer()]) #Odbieraj wiadomości | asynchroniczne


# data=[0x01, 0x02, 0x03, 0x04, 0x05, 0x06, 0x07, 0x08, 0x09, 0x0A]




timeout_rcv = 3  
flag=0

while(True):
    for dev in devices:
        msg=getHeartbeatSnd(dev.id)
        print("OUT ", msg)
        bus.send(msg, timeout=1)
        start = time.time()
        flag=0  
        while time.time() - start < timeout_rcv:
            msg=bus.recv(timeout=timeout_rcv)
            print("IN ", msg)
            if(msg!=None and msg.arbitration_id == getHeartbeatRcv(dev.id).arbitration_id and msg.data == getHeartbeatRcv(dev.id).data):
                flag=1
                switchOn(msg.arbitration_id)
        print("-------------------------------")
        for dev in devices:
            print(dev)
        print("-------------------------------")