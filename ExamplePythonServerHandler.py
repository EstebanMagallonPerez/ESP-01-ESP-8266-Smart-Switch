import socket
import json
import threading
import time

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
        try:
            output = self.sendHandler(data=b"3")
            data = json.loads(output)
            if "state" in data:
                return data["state"]
        except:
            return None
        return None
    
    def sendUpdate(self,data):
        x = threading.Thread(target=lambda: self.sendHandler(data=data))
        x.start()
    
    def sendHandler(self,data):
        BUFFER_SIZE = 1024
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            s.settimeout(1)
            s.connect((self.ip, self.port))
            s.send(data)
            data = s.recv(BUFFER_SIZE)
            s.close()
            decodedData = data.decode('utf-8')
            data = json.loads(decodedData)
            self.stateCallback(data)
        except:
            return None
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
    tcpServer = None
    def __init__(self,host,port):
        self.host = host
        self.port = port
        print("starting with:", host,port)

    def start(self):
        self.tcpServer = threading.Thread(target=self.listener)
        self.tcpServer.start()
        self.tcpServerWatcher = threading.Thread(target=self.keepAlive)
        self.tcpServerWatcher.start()

    def keepAlive(self):
        while 1:
            if not self.tcpServer.is_alive():
                self.tcpServer = threading.Thread(target=self.listener)
                self.tcpServer.start()
            time.sleep(10)
        
    
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
                            decodedData = data.decode('utf-8').replace('\x00', '')
                            print("decoded data", data, decodedData)
                            data = json.loads(decodedData)
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
