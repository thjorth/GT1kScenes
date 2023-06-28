
MAX_EFFECTS = 10

class Scene():
	def __init__(self, index):
		self.effects = [False, False, False, False, False, False, False, False, False, False]
		self.vol = 21 # goes from -20dB to +20dB, both numbers included, so 21 is 0dB
		self.cc1 = -1
		self.cc2 = -1
		self.cc3 = -1
		self.ext_pc = -1
		self.ext_cc = -1
		self.index = index
		
	def update_effect(self, index, status):
		if index < MAX_EFFECTS:
			self.effects[index] = status
		print(self.effects)


			