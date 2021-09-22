import pickle

class Packet:
	def unpack(self, data):
		data = pickle.loads(data)
		return data

	def pack(self, data):
		data = pickle.dumps(data)
		return data