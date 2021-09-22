import socket
import asyncio
from prompt_toolkit import PromptSession
from prompt_toolkit.patch_stdout import patch_stdout

client = socket.socket()
client.connect(('localhost', 5050))
client.setblocking(False)

async def recv():
	while True:
		try:
			message = client.recv(64)
			print(message.decode())
		except: 
			pass
		await asyncio.sleep(1/20)

async def send():
	session = PromptSession("Say something : ")
	while True:
		message = await session.prompt_async()
		client.send(message.encode())
		await asyncio.sleep(1/10)

async def main():
	with patch_stdout():
		task = asyncio.create_task(recv())
		try:
			await send()
		finally:
			task.cancel()

asyncio.run(main())