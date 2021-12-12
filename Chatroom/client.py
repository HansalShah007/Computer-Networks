import socket
import threading

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(('localhost', 9999))
nickname = input("Enter a nickname: ")
wants_to_exit = False

def receive():
	global wants_to_exit
	while not wants_to_exit:
		try:
			message = (client.recv(1024)).decode('ascii')
			if(message=='nick'):
				client.send(nickname.encode('ascii'))
			else:
				print(message)
		except:
			print("Something went wrong!")
			client.close()
			break

def send():
	global wants_to_exit
	while not wants_to_exit:
		content = input()
		message = f'{nickname}: {content}'
		if(content.lower()=='exit'):
			print("Disconnected from the server!")
			client.send((content.lower()).encode('ascii'))
			wants_to_exit = True
		else:
			client.send(message.encode('ascii'))


rthread = threading.Thread(target=receive)
rthread.start()

sthread = threading.Thread(target=send)
sthread.start()
