from threading import *
import socket

receiver = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
receiver.connect(('localhost',10000))

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

def convert_from_bin(message_bin):
    message_bin = ''.join(message_bin)
    message = ''
    for i in range(0,len(message_bin),7):
        character = message_bin[i:i+7]
        character = chr(int(character,2))
        message+=character
    return message

def checksum_check(message_bin, checksum_bin):

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
            
    addition = add(addition, checksum_bin)
    
    if '0' in addition:
        print('The message is corrupted!')
        ack = "Corrupted message is recieved, please send again".encode('ascii')
        receiver.send(ack)
    else:
        print('The message is not corrupted.')
        print("Received --> "+convert_from_bin(message_bin))
        ack = "Acknowledgement: Message received".encode('ascii')
        receiver.send(ack)

while True:
    try:
        message_bin = receiver.recv(1024).decode('ascii')
        checksum_bin = receiver.recv(1024).decode('ascii')
        checksum_check(message_bin, checksum_bin)
    except:
        print("Sender disconnected!")
        receiver.close()
        break