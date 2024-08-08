import socket
import json
import threading

class customDeviceAPI:
    shouldHighlight = True
    ip = None
    port = None
    stateCallback = None

    def __init__(self, ip, port):
        self.ip = ip
        self.port = port

    def off(self):
        self.sendUpdate(b"0")
    
    def on(self):
        self.sendUpdate(b"1")
    
    def toggle(self):
        self.sendUpdate(b"2")

    def getState(self):
        output = self.sendHandler(data=b"3")
        #print("state from handler is:", output)
        if output == b'\x01':
            return True
        if output == b'\x00':
            return False
        return False
    
    
    def sendUpdate(self,data):
        x = threading.Thread(target=lambda: self.sendHandler(data=data))
        x.start()
    
    def sendHandler(self,data):
        #print("async handling of send:", self.ip, data)
        BUFFER_SIZE = 1024
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((self.ip, self.port))
        s.send(data)
        data = s.recv(BUFFER_SIZE)
        s.close()
        return data

class pairedDevices:
    devices  = None
    def __init__(self):
        self.devices = {}
        try:
            with open('devices.json', 'r') as openfile:
                # Reading from json file
                self.devices = json.load(openfile)
        except:
            with open('devices.json', 'w', encoding='utf-8') as f:
                json.dump(self.devices, f, ensure_ascii=False, indent=4)
    
    def getPairedDevices(self):
        return self.devices
    
    def addPairedDevice(self, device):
        self.devices[device["name"]] = {"name":device["name"],"ip":device["ip"]}
        with open('devices.json', 'w', encoding='utf-8') as f:
            json.dump(self.devices, f, ensure_ascii=False, indent=4)
    

class deviceManager:
    host = None
    port = None
    callback = None
    pairList = pairedDevices()
    def __init__(self,host,port):
        self.host = host
        self.port = port
        print("starting with:", host,port)

    def start(self):
        x = threading.Thread(target=self.listener)
        x.start()
    
    def setEventCallback(self,callback):
        self.callback = callback


    def listener(self):
        while 1:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.bind((self.host, self.port))
                s.listen()
                conn, addr = s.accept()
                with conn:
                    while True:
                        data = conn.recv(1024)
                        if data:
                            decodedData = data.decode('utf-8')
                            data = json.loads(decodedData[:-1])
                            data['ip'] = addr[0]
                            if data['name'] not in self.pairList.devices:
                                self.pairList.addPairedDevice(data)
                            self.callback(data)
                        elif not data:
                            break
                    conn.sendall(data)
'''
SERVER_HOST = '192.168.1.50'
SERVER_PORT = '80'
CUSTOM_PORT = 4444

device = customDeviceAPI('192.168.1.148',4444)

deviceListener = deviceManager(SERVER_HOST,CUSTOM_PORT)
deviceListener.setEventCallback(print)
deviceListener.start()
'''
