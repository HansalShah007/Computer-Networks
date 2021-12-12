import threading
from threading import *
import socket

sender = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sender.bind(('localhost', 10000))

sender.listen()
print("Sender is listening...")

def add(a,b):
    ans = ''    
    carry ='0'
    for _ in range(len(a)-1,-1,-1):
        total = int(a[_])+int(b[_])+int(carry)
        if total==0:
            ans+='0'
            carry='0'
        elif total==1:
            ans+='1'
            carry='0'
        elif total==2:
            ans+='0'
            carry='1'
        elif total==3:
            ans+='1'
            carry+='1'
    
    if carry=='1':
        return add(ans, ('0'*6)+'1')
    return ans

def ones_complement(message_bin):
    complement = ''
    for character in message_bin:
        if character=='0':
            complement+='1'
        else:
            complement+='0'
    return complement

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

def checksum_gen(message):
    message_bin = convert_to_bin(message)
    
    segments = []
    addition = ''
    for i in range(0,len(message_bin),7):
        segments.append(message_bin[i:i+7])
    
    if len(segments)==1:
        addition = segments[0]
    else:
        addition = add(segments[0],segments[1])
        
        for _ in range(2,len(segments)):
            addition = add(addition,segments[_])
    
    return message_bin, ones_complement(addition)
    

def handle_receiver(receiver):
    connected = True
    
    while connected:
        r = input("Send data --> ")
        
        if r.lower() == 'exit':
            connected = False
            receiver.close()
        else:
            message_bin, checksum_bin = checksum_gen(r)
            receiver.send(message_bin.encode('ascii'))
            receiver.send(checksum_bin.encode('ascii'))
            print(receiver.recv(1024).decode('ascii'))
    return False

listening = True
while listening:
    receiver, address = sender.accept()
    print("Receiver "+str(address)+" connected!")

    t = threading.Thread(target=handle_receiver, args=[receiver])
    listening = t.start()


