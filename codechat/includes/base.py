import os
import socket
import select
import signal
from packets import Packet

class Server:
	def __init__(self, ip):
		# CONFIGS
		self.IP = ip
		self.PORT = 5050
		# SERVER SETTINGS
		self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
		self.server.bind((self.IP, self.PORT))
		self.server.listen()
		print(' [*] server running on {}:{}'.format(self.IP, self.PORT))
		# HEADERS 
		self.packet = Packet()
		# FLAGS 
		self.running = True
		# CONNECTIONS
		self.connections = [self.server]
		# HEADER
		self.HEADER_LENGTH = 10

	def receive(self, client):
		try:
			message = client.recv(322)
			if not len(message):
				return False
			message = self.packet.unpack(message)
			return message
		except: 
			return False

	def send(self, message, client):
		message = self.packet.pack(message)
		for connection in self.connections:
			if connection != client and connection != self.server:
				connection.send(message)

	def delete(self, closed_socket):
		self.connections.remove(closed_socket)
		print(" [x] closed connection...")

	def run(self):
		while self.running:
			connections, _, execptions = select.select(self.connections, [],
				self.connections)
			for connection in connections:
				if connection == self.server:
					client, addr = self.server.accept()
					user_data = self.receive(client)
					if user_data is False:
						continue
					self.connections.append(client)
					print(f" > {user_data['username']} with {addr[0]}:{addr[1]}")
				else:
					message = self.receive(connection)
					if message is False:
						self.delete(connection)
						continue
					self.send(message, connection)
			for closed_socket in execptions:
				self.delete(closed_socket)

	def _exit(self):
		self.running = False
		for connection in self.connections:
			connection.close()
		self.server.close()
		input(" [x] server closed...\n press [ENTER] to exit...")

IP = socket.gethostbyname(socket.gethostname())
server = Server(IP)
signal.signal(signal.SIGINT, server._exit)
server.run()