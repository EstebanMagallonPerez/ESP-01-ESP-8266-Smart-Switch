import network
import socket
import time
import json
import _thread
import machine
from machine import Pin

deviceName = "pythonDevice"
SSID = 'SSID'
PASS  = 'PASSWORD'
SERVER_IP = '192.168.1.50'
SERVER_PORT = 4444

button = Pin(5, Pin.IN, Pin.PULL_UP)
led = Pin(15, Pin.OUT)
relay = Pin(3, Pin.OUT)
BUFFER_SIZE = 1024
lastVal = 1
state = 0


sta_if = network.WLAN(network.STA_IF)   
def do_connect():
    led.value(1)
    if not sta_if.isconnected():
        print('connecting to network...')
        sta_if.active(True)
        sta_if.connect(SSID, PASS)
        while not sta_if.isconnected():
            pass
    print('network config:', sta_if.ifconfig())
    led.value(0)

def socketListener():
    global counter
    addr = socket.getaddrinfo(sta_if.ifconfig()[0], 4444)[0][-1]
    s = socket.socket()
    s.bind(addr)
    s.listen()
    while counter < 15:
        cl, addr = s.accept()
        data = cl.recv(1024)
        if data == b"0":
            setState(False)
        if data == b"1":
            setState(True)
        if data == b"2":
            toggle()
        cl.send(msgToSend())
        cl.close()
    s.close()
    print("exiting thread")

def sendMsg():
    sendSocket = socket.socket()
    sendSocket.settimeout(1)
    sendSocket.connect((SERVER_IP, SERVER_PORT))
    sendSocket.send(msgToSend())
    sendSocket.close()
    
def msgToSend():
    global state
    msgData = {"name":deviceName,"ip": sta_if.ifconfig()[0],"state":state}
    return str.encode(json.dumps(msgData))

def setState(value):
    global state
    state = value

def toggle():
    setState(not state)
    

do_connect()
_thread.start_new_thread(socketListener, ())

counter = 0

while counter < 20:
    led.value(state)
    relay.value(state)
    time.sleep(.1)
    if button.value() == 0 and lastVal == 1:
        print("sending message")
        toggle()
        _thread.start_new_thread(sendMsg, ())
        lastVal = 0
    elif lastVal == 0 and button.value() == 1:
        print("resetting things")
        lastVal = 1
        counter = 0
    elif button.value() == 0:
        counter += 1

print("rebooting device")
time.sleep(3)
machine.reset()
        
    

