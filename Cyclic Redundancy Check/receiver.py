from threading import *
import socket

receiver = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
receiver.connect(('localhost',10000))

def xor(a,b):
    
    ans = ''    
    for _ in range(len(a)):
        if(a[_]==b[_]):
            ans+='0'
        else:
            ans+='1'
    return ans

def convert_from_bin(message_bin):
    message_bin = ''.join(message_bin)
    message = ''
    for i in range(0,len(message_bin),7):
        character = message_bin[i:i+7]
        character = chr(int(character,2))
        message+=character
    return message

def crc_check(padded_message, polynomial_bin):
    
    dividend = list(padded_message)
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
        
    if '1' in remainder:
        print('The message is corrupted!')
        ack = "Corrupted message is recieved, please send again".encode('ascii')
        receiver.send(ack)
    else:
        print('The message is not corrupted.')
        print("Received --> "+convert_from_bin(padded_message[0:len(padded_message)-len(polynomial_bin)+1]))
        ack = "Acknowledgement: Message received".encode('ascii')
        receiver.send(ack)

while True:
    polynomial_bin = '11010'
    try:
        message = receiver.recv(1024).decode('ascii')
        crc_check(message, polynomial_bin)
    except:
        print("Sender disconnected!")
        receiver.close()
        break