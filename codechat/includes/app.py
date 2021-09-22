from __future__ import unicode_literals, print_function
import socket
import asyncio
import signal
import sys
from packets import Packet
from prompt_toolkit import PromptSession
from prompt_toolkit.patch_stdout import patch_stdout

class Debug:
	def write(self, msg):
		pass

class Client:
	def __init__(self):
		# CONFIGS
		self.IP = str(input("[HOST] > "))
		self.PORT = 5050
		# CLIENT
		self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		# FLAGS
		self.running = True
		# HEADER LENGTH
		self.HEADER_LENGTH = 10
		# LOADING HEADERS
		self.packet = Packet()
		# TEMPLATE
		self.user = { "username" : "", "content" : "" }
		self.connected = True
		try:
			self.client.connect((self.IP, self.PORT))
			self.client.setblocking(False)
		except:
			self.connected = False
		self.register()

	def register(self):
		self.user['username'] = input(" username > ")
		content = self.packet.pack(self.user)
		self.client.send(content)

	async def receive(self):
		while self.running:
			try:
				message = self.client.recv(322)
				message = self.packet.unpack(message)
				print(" [{}] : {}".format(message['username'], 
					message['content']))
			except:
				pass
			await asyncio.sleep(1/20)	
			
	async def send(self):
		session = PromptSession(" [You] : ")
		while self.running:
			content = self.user
			content['content'] = await session.prompt_async()
			content = self.packet.pack(content)
			self.client.send(content)
			await asyncio.sleep(1/10)
	
	async def main(self):
		with patch_stdout():
			reciever = asyncio.create_task(self.receive())
			try:
				await self.send()
			finally:
				reciever.cancel()

	def _exit(self, signal, _exit):
		self.running = False
		client.client.close()
		
sys.stderr = Debug()
client = Client()
signal.signal(signal.SIGINT, client._exit)
asyncio.run(client.main())
input(' press [ENTER] to continue...')

