from threading import *
import socket

receiver = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
receiver.connect(('localhost',10000))

while True:
    try:
        message = receiver.recv(1024).decode('ascii')
        print("Received --> "+str(message))
        ack = "Acknowledgement: Message received".encode('ascii')
        receiver.send(ack)
    except:
        print("Sender disconnected!")
        receiver.close()
        break