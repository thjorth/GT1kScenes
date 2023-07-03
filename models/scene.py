
MAX_EFFECTS = 10

class Scene():
	def __init__(self, index):
		self.effects = [False, False, False, False, False, False, False, False, False, False]
		self.vol = 21 # goes from -20dB to +20dB, both numbers included, so 21 is 0dB
		self.cc1 = -1
		self.cc2 = -1
		self.ext_pc = -1
		self.ext_cc = -1
		self.index = index
		
	def update_effect(self, index, status):
		if index < MAX_EFFECTS:
			self.effects[index] = status
		print(self.serialize())

	def update_volume(self, volume):
		self.vol = volume.value
		print(self.serialize())

	def update_cc(self, cc):
		if cc.id == "cc1":
			self.cc1 = cc.value
		elif cc.id == "cc2":
			self.cc2 = cc.value
		elif cc.id == "ext_cc":
			self.ext_cc = cc.value
		print(self.serialize())

	def update_pc(self, pc):
		self.ext_pc = pc.value

	def serialize(self):
		s = ""
		i = 0
		while i < MAX_EFFECTS:
			if self.effects[i]:
				s += "1"
			else:
				s += "0"
			i += 1
		s += " " + str(self.vol)
		s += " " + str(self.cc1)
		s += " " + str(self.cc2)
		s += " " + str(self.cc3)
		s += " " + str(self.ext_pc)
		s += " " + str(self.ext_cc)
		return s
	
	def deserialize(self, s):
		parts = s.split()
		# first let's deserialize the effects on/off statuses
		i = 0
		status_bits = parts[0]
		while i < len(status_bits):
			if status_bits[i] == '1':
				self.effects[i] = True
			else:
				self.effects[i] = False
			i += 1
		self.vol = int(parts[1])
		self.cc1 = int(parts[2])
		self.cc3 = int(parts[3])
		self.ext_pc = int(parts[4])
		self.ext_cc = int(parts[5])
		

			