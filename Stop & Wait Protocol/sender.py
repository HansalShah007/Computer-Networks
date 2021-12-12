import threading
from threading import *
import socket

sender = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sender.bind(('localhost', 10000))

sender.listen()
print("Sender is listening...")


def handle_receiver(receiver):
    connected = True
    while connected:
        r = input("Send data --> ")
        if r.lower() == 'exit':
            connected = False
            receiver.close()
        else:
            receiver.send(r.encode('ascii'))
            print(receiver.recv(1024).decode('ascii'))
    return False


listening = True
while listening:
    receiver, address = sender.accept()
    print("Receiver "+str(address)+" connected!")

    t = threading.Thread(target=handle_receiver, args=[receiver])
    listening = t.start()


