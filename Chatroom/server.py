import socket
import threading

host = ''
port = 9999

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((host, port))
server.listen()

clients = {}
superuser = []

def broadcast(message):
	for client in clients:
		client.send(message)

def handle_client(client):
	wants_to_exit = False
	while not wants_to_exit:
		try:
			message = client.recv(1024)
			if(message.decode('ascii')=='exit'):
				broadcast(f'{clients[client]} has left the chat.'.encode('ascii'))
				clients.pop(client)
				client.close()
				wants_to_exit=True
			else:
				broadcast(message)
		except:
			broadcast(f'{clients[client]} has left the chat.'.encode('ascii'))
			clients.pop(client)
			client.close()
			break

def start_listening():
	while True:
		client, addr = server.accept()
		print(f'Connected to {addr}')

		client.send('nick'.encode('ascii'))
		nickname = (client.recv(1024)).decode('ascii')
		clients[client] = nickname
		broadcast(f'{nickname} has joined the chat'.encode('ascii'))
		client.send('Connected to the server!'.encode('ascii'))

		t = threading.Thread(target=handle_client, args=[client])
		t.start()

print('Sever is listening')
start_listening()
