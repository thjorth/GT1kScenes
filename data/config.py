from os.path import exists

import json

FILE_NAME = "config.json"

DEFAULT_CONFIG = {
	"devices": {
		"main_midi_device": "UM-ONE",
		"scene_select_midi_device": "SparkFun", 
	}
}

class Config():
	def __init__(self):
		# nothing to init yet
		if not exists(FILE_NAME):
			with open(FILE_NAME, "w") as f:
				json.dump(DEFAULT_CONFIG, f)
		
		data = None
		with open(FILE_NAME, "r") as f:
			data = json.load(f)
		if data:
			self.main_midi_device = data["devices"]["main_midi_device"]
			self.scene_select_midi_device = data["devices"]["scene_select_midi_device"]

		print(self.main_midi_device, self.scene_select_midi_device)

	