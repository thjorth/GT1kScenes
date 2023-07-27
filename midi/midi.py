import rtmidi
import time
from midi.dummy import Dummy
import mido
from data.config import Config

CONFIG = Config()

mido.set_backend('mido.backends.pygame')
outs = mido.get_output_names()
print("outs: ", outs)

from rtmidi.midiconstants import (
	PROGRAM_CHANGE,
	CONTROL_CHANGE
)
from rtmidi import midiutil

import singleton

MIDI_DEVICE = CONFIG.main_midi_device
SCENE_CHANGE_DEVICE = CONFIG.scene_select_midi_device
EFFECT_CC_START = 71
CC_VOL = 81
CC1 = 82
CC2 = 83
CC_EXT = 7

NUMBER_OF_EFFECTS = 10
NUMBER_OF_SYSX_EFFECTS = 6

# the channel that is used for changing scenes within a preset
MIDI_SCENE_SELECT_CHANNEL = 0
MIDI_EFFECTS_CHANNEL = 0
MIDI_EXT_CHANNEL = 1

index_to_cc_map = [71, 72, 73, 75, 76, 74, 77, 78, 79, 80]

index_to_fx_name_map = ['comp', 'dist1', 'dist2', 'mdelay', 'delay', 'chorus', 'fx1', 'fx2', 'fx3', 'fx4']
fx_sysx_map = {
	'comp':		('F0 41 00 00 00 00 4F 12 10 00 12 00 01 5D F7', 'F0 41 00 00 00 00 4F 12 10 00 12 00 00 5E F7'),	
	'dist1':	('F0 41 00 00 00 00 4F 12 10 00 13 00 01 5C F7', 'F0 41 00 00 00 00 4F 12 10 00 13 00 00 5D F7'),
	'dist2':	('F0 41 00 00 00 00 4F 12 10 00 14 00 01 5B F7', 'F0 41 00 00 00 00 4F 12 10 00 14 00 00 5C F7'),
	'mdelay':	('F0 41 00 00 00 00 4F 12 10 00 21 00 01 4E F7', 'F0 41 00 00 00 00 4F 12 10 00 21 00 00 4F F7'),
	'delay':	('F0 41 00 00 00 00 4F 12 10 00 1D 00 01 52 F7', 'F0 41 00 00 00 00 4F 12 10 00 1D 00 00 53 F7'),
	'chorus':	('F0 41 00 00 00 00 4F 12 10 00 22 00 01 4D F7', 'F0 41 00 00 00 00 4F 12 10 00 22 00 00 4E F7'),
	'fx1':		('F0 41 00 00 00 00 4F 12 10 00 23 00 01 4C F7', 'F0 41 00 00 00 00 4F 12 10 00 23 00 00 4D F7'),
	'fx2':		('F0 41 00 00 00 00 4F 12 10 00 3E 00 01 31 F7', 'F0 41 00 00 00 00 4F 12 10 00 3E 00 00 32 F7'),
	'fx3':		('F0 41 00 00 00 00 4F 12 10 00 59 00 01 16 F7', 'F0 41 00 00 00 00 4F 12 10 00 59 00 00 17 F7'),
	'fx4':		('F0 41 00 00 00 00 4F 12 10 02 01 00 01 6C F7', 'F0 41 00 00 00 00 4F 12 10 02 01 00 00 6D F7'),
}

TUNER_ON = 'F0 41 00 00 00 00 4F 12 7F 00 00 02 01 7E F7'
TUNER_OFF = 'F0 41 00 00 00 00 4F 12 7F 00 00 02 00 7F F7'

# MAYBE edit mode on/off
EDIT_MODE_ON  = 'F0 41 00 00 00 00 4F 12 7F 00 00 01 01 7F F7'
EDIT_MODE_OFF = 'F0 41 00 00 00 00 4F 12 7F 00 00 01 00 00 F7'

# EQ 3 level
# F0 41 00 00 00 00 4F 12 10 00 1B 04 0C 45 F7 (-20 dB)
# F0 41 00 00 00 00 4F 12 10 00 1B 04 0D 44 F7 (-19 dB)
# F0 41 00 00 00 00 4F 12 10 00 1B 04 20 31 F7 (  0 dB)
# F0 41 00 00 00 00 4F 12 10 00 1B 04 21 30 F7 ( +1 dB)
# 


class Midi(singleton.SingletonClass):
	def __init__(self):
		self.timer = time.time()
		self.preset = None
		# get our MIDI connections set up
		self.midiout_index = -1
		self.midiin_index = -1

		available_out_ports = mido.get_output_names()
		i = 0
		self.midiout = None
		while i < len(available_out_ports):
			if available_out_ports[i].startswith(MIDI_DEVICE) and not self.midiout:
				self.midiout_index = i
				print("out: ", available_out_ports[i])
				self.midiout = mido.open_output(available_out_ports[i])
			i += 1

		available_in_ports = mido.get_input_names()
		print("ins: ", available_in_ports)
		self.scene_selector_midiin = None
		self.midiin = None
		i = 0
		while i < len(available_in_ports):
			if available_in_ports[i].startswith(MIDI_DEVICE) and not self.midiin:
				self.midiin_index = i
				print("in:  ", available_in_ports[i])
				self.midiin = mido.open_input(available_in_ports[i])
			if available_in_ports[i].startswith(SCENE_CHANGE_DEVICE) and not self.scene_selector_midiin:
				self.scene_selector_midiin = mido.open_input(available_in_ports[i])
			i += 1

		if not self.midiin:
			self.midiin = Dummy()
		if not self.scene_selector_midiin:
			self.scene_selector_midiin = Dummy()

	def __del__(self):
		# self.midiout.close()
		# self.midiin.close()
		# del self.midiout
		# del self.midiin
		pass

	def edit_mode_on(self):
		# if self.midiout:
		# 	edit_mode_msg = mido.Message.from_hex(EDIT_MODE_ON)
		# 	self.midiout.send(edit_mode_msg)
		# 	time.sleep(0.02)
		pass

	def edit_mode_off(self):
		# if self.midiout:
		# 	time.sleep(0.2)
		# 	edit_mode_msg = mido.Message.from_hex(EDIT_MODE_OFF)
		# 	self.midiout.send(edit_mode_msg)
		# 	time.sleep(0.1)
		pass


	def send(self, msg):
		if self.midiout and not self.midiout.closed:
			print(msg)
			self.midiout.send(msg)
			time.sleep(0.01)

	def respond(self):
		# First respond to the messages coming in on the normal midi in and make sure that they are sent through to midiout
		msg = self.midiin.poll()
		if msg:
			print(msg)
			if msg.type != "sysex" and msg.channel != 0:
				# now write these messages to the midi out to allow midi to pass through if it was not transmitted on channel 0
				self.send(msg)

			# check if there is a PC on channel 0. If there is, then switch to another preset
			if msg.type == "program_change" and msg.channel == 0:
				self.preset.select_preset(msg.program)

			if msg.type == "control_change" and msg.channel == 0 and msg.control >= 1 and msg.control <= 6 and msg.value == 127:
				self.preset.select_scene(msg.control - 1)

			if self.is_patch_change_sysex(msg):
				# The program number is hidden in msg.data[12]
				self.edit_mode_on()
				self.preset.select_preset(msg.data[12])
				self.edit_mode_off()

		# now check the scene selector midi in to see if there is something that needs to be handled
		pc = self.scene_selector_midiin.poll()
		if pc:
			# select a new scene
			self.preset.select_scene(pc.program)

		return False

	def is_patch_change_sysex(self, msg):
		# example patch change sysex: 
		# 65,0,0,0,0,79,18,127,0,1,0,0,1,127
		if msg.type != "sysex":
			return False
		if len(msg.data) != 14:
			return False
		d = msg.data
		if d[0] == 0x41 and d[5] == 0x4F and d[6] == 0x12 and d[7] == 0x7F and d[8] == 0x0 and d[9] == 0x1 and d[10] == 0x0 and d[11] == 0x0:
			return True
		
		return False

	def set_preset(self, preset):
		self.preset = preset

	def output_scene(self, scene, old_scene):
		i = 0
		print("old_scene:", old_scene)
		print("scene:", scene)

		self.edit_mode_on()
		# effects on/off
		while i < NUMBER_OF_EFFECTS:
			if not old_scene or old_scene.effects[i] != scene.effects[i]:
				if i < NUMBER_OF_SYSX_EFFECTS:
					fxname = index_to_fx_name_map[i]
					if scene.effects[i]:
						msg = mido.Message.from_hex(fx_sysx_map[fxname][0])
					else:
						msg = mido.Message.from_hex(fx_sysx_map[fxname][1])
					self.send(msg)
				else:
					cc = index_to_cc_map[i]
					if scene.effects[i]:
						value = 127
					else:
						value = 0
					msg = mido.Message('control_change', channel=MIDI_EFFECTS_CHANNEL, control=cc, value=value)
					self.send(msg)
			i += 1

		# volume
		if (not old_scene or old_scene.vol != scene.vol) and scene.vol != -1:
			sysex_vol = 0x0C + scene.vol + 20
			checksum = 81 - sysex_vol
			data = "F0 41 00 00 00 00 4F 12 10 00 1B 04 {0:02x} {1:02x} F7".format(sysex_vol, checksum)
			msg = mido.Message.from_hex(data)
			self.send(msg)

		# cc1
		if (not old_scene or old_scene.cc1 != scene.cc1) and scene.cc1 != -1:
			msg = mido.Message('control_change', channel=MIDI_EFFECTS_CHANNEL, control=CC1, value=scene.cc1)
			self.send(msg)

		# cc2
		if (not old_scene or old_scene.cc2 != scene.cc2) and scene.cc2 != -1:
			msg = mido.Message('control_change', channel=MIDI_EFFECTS_CHANNEL, control=CC2, value=scene.cc2)
			self.send(msg)

		# External PC (for switching ToneX presets)
		if (not old_scene or old_scene.ext_pc != scene.ext_pc) and scene.ext_pc != -1:
			msg = mido.Message('program_change', channel=MIDI_EXT_CHANNEL, program=scene.ext_pc)
			self.send(msg)

		self.edit_mode_off()

	def output_effect(self, effect):
		self.edit_mode_on()

		fxname = index_to_fx_name_map[effect.index]
		if effect.enabled:
			msg = mido.Message.from_hex(fx_sysx_map[fxname][0])
		else:
			msg = mido.Message.from_hex(fx_sysx_map[fxname][1])
		self.send(msg)

		self.edit_mode_off()

	def output_volume(self, volume):
		self.edit_mode_on()

		sysex_vol = 0x0C + volume.value + 20
		checksum = 81 - sysex_vol
		data = "F0 41 00 00 00 00 4F 12 10 00 1B 04 {0:02x} {1:02x} F7".format(sysex_vol, checksum)
		msg = mido.Message.from_hex(data)
		self.send(msg)

		self.edit_mode_off()

	def output_cc(self, cc):
		self.edit_mode_on()

		if cc.value >= 0 and cc.value < 128:
			if cc.id == "cc1":
				msg = mido.Message('control_change', channel=MIDI_EFFECTS_CHANNEL, control=CC1, value=cc.value)
			elif cc.id == "cc2":
				msg = mido.Message('control_change', channel=MIDI_EFFECTS_CHANNEL, control=CC2, value=cc.value)
			elif cc.id == "ext_cc":
				msg = mido.Message('control_change', channel=MIDI_EFFECTS_CHANNEL, control=CC_EXT, value=cc.value)

			if msg:
				self.send(msg)

		self.edit_mode_off()

	def output_pc(self, pc):
		self.edit_mode_on()
		if pc.value >= 0 and pc.value < 128:
			if pc.id == "ext_pc":
				msg = mido.Message('program_change', channel=MIDI_EXT_CHANNEL, program=pc.value)
				self.send(msg)
		self.edit_mode_off()
			
					


