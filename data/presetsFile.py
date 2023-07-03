from os.path import exists

EMPTY_PRESET = "0000000000 0 -1 -1 -1 -1::0000000000 0 -1 -1 -1 -1::0000000000 0 -1 -1 -1 -1::0000000000 0 -1 -1 -1 -1::0000000000 0 -1 -1 -1 -1::0000000000 0 -1 -1 -1 -1::\n"
MAX_PRESETS = 250
FILE_NAME = "presets.txt"

class PresetsFile():
	def __init__(self):
		self.lines = []
		self.active_preset_index = 0
		
		if exists(FILE_NAME):
			file1 = open(FILE_NAME, "r")
			self.lines = file1.readlines()
			file1.close()
		while len(self.lines) < MAX_PRESETS:
			self.lines.append(EMPTY_PRESET)
		print(self.lines)

	def select_preset(self, index):
		self.active_preset_index = index

	def update_active_preset(self, str):
		self.lines[self.active_preset_index] = str

	def get_active_preset(self):
		return self.lines[self.active_preset_index]
	
	def save(self):
		file1 = open(FILE_NAME, "w")
		for line in self.lines:
			file1.write(line)
		file1.close()
