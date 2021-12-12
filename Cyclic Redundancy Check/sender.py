import threading
from threading import *
import socket

sender = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sender.bind(('localhost', 10000))

sender.listen()
print("Sender is listening...")

def xor(a,b):
    
    ans = ''    
    for _ in range(len(a)):
        if(a[_]==b[_]):
            ans+='0'
        else:
            ans+='1'
    return ans


def convert_to_bin(message):
    
    binaries = []
    for _ in range(len(message)):
        temp = ord(message[_])
        temp = bin(temp).replace('0b','')
        
        shift = 7-len(temp)
        temp = ('0'*shift)+temp
        
        binaries.append(temp)
    
    message_bin = ''.join(binaries)
    return message_bin

def crc_gen(message, polynomial_bin):
    message_bin = convert_to_bin(message)
    padded_message = list(message_bin+('0'*(len(polynomial_bin)-1)))
    dividend = padded_message.copy()
    remainder = None
    
    while True:
        try:
            index_1 = dividend.index('1')
        except:
            remainder = ['0' for _ in range(len(polynomial_bin)-1)]
            break
        
        if index_1<=len(dividend)-len(polynomial_bin):           
            part = dividend[index_1:index_1+len(polynomial_bin)]
            dividend[index_1:index_1+len(polynomial_bin)] = xor(part,polynomial_bin)
        else:
            remainder = dividend[len(dividend)-len(polynomial_bin)+1:]
            break

    padded_message[len(dividend)-len(polynomial_bin)+1:] = remainder
    return ''.join(padded_message)


def handle_receiver(receiver):
    polynomial_bin = '11010'
    connected = True
    
    while connected:
        r = input("Send data --> ")
        
        if r.lower() == 'exit':
            connected = False
            receiver.close()
        else:
            r = crc_gen(r, polynomial_bin)
            receiver.send(r.encode('ascii'))
            print(receiver.recv(1024).decode('ascii'))
    return False

listening = True
while listening:
    receiver, address = sender.accept()
    print("Receiver "+str(address)+" connected!")

    t = threading.Thread(target=handle_receiver, args=[receiver])
    listening = t.start()


