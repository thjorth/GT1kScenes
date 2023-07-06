import rtmidi
import time
from rtmidi.midiconstants import (
    PROGRAM_CHANGE,
    CONTROL_CHANGE
)
from rtmidi import midiutil

import singleton

MIDI_DEVICE = "UM-ONE"
EFFECT_CC_START = 71
CC_VOL = 81
CC1 = 82
CC2 = 83
CC_EXT = 7

NUMBER_OF_EFFECTS = 10

# the channel that is used for changing scenes within a preset
MIDI_SCENE_SELECT_CHANNEL = 0
MIDI_EFFECTS_CHANNEL = 0
MIDI_EXT_CHANNEL = 1

index_to_cc_map = [71, 72, 73, 75, 76, 74, 77, 78, 79, 80]

api = midiutil.get_api_from_environment()
print("api: ", api)
class Midi(singleton.SingletonClass):
	def __init__(self):
		self.timer = time.time()
		self.preset = None
		# get our MIDI connections set up
		self.midiout_index = -1
		self.midiin_index = -1

		#self.midiout = rtmidi.MidiOut(rtapi=rtmidi.API_LINUX_ALSA)
		self.midiout = rtmidi.MidiOut()
		available_out_ports = self.midiout.get_ports()
		print("available outports:")
		print(available_out_ports)
		i = 0
		found = False
		while i < len(available_out_ports) and not found:
			if available_out_ports[i].startswith(MIDI_DEVICE):
				self.midiout_index = i
				found = True
			i += 1

		if (self.midiout_index >= 0):
			print("MIDI out:", available_out_ports[self.midiout_index])
			self.midiout.open_port(self.midiout_index)

		#self.midiin = rtmidi.MidiIn(rtapi=rtmidi.API_LINUX_ALSA)
		self.midiin = rtmidi.MidiIn()
		available_in_ports = self.midiin.get_ports()
		print("available inports:")
		print(available_in_ports)
		i = 0
		found = False
		while i < len(available_in_ports) and not found:
			if available_in_ports[i].startswith(MIDI_DEVICE):
				self.midiin_index = i
				found = True
			i += 1

		if (self.midiin_index >= 0):
			print("MIDI in:", available_in_ports[self.midiin_index])
			self.midiin.open_port(self.midiin_index)

		print("(PROGRAM_CHANGE | MIDI_SCENE_SELECT_CHANNEL):", (PROGRAM_CHANGE | MIDI_SCENE_SELECT_CHANNEL))


	def __del__(self):
		self.midiout.close_port()
		self.midiin.close_port()
		del self.midiout
		del self.midiin

	def respond(self):
		msg = self.midiin.get_message()
		if msg:
			message, deltatime = msg
			self.timer += deltatime
			print("@%0.6f %r" % (self.timer, message))
			# now write these messages to the midi out to allow midi to pass through
			self.midiout.send_message(message)

			# now check if we need to do something with the incoming message
			if message[0] == (PROGRAM_CHANGE | MIDI_EFFECTS_CHANNEL):
				self.preset.select_scene(message[1])
				return True
		return False

	def set_preset(self, preset):
		self.preset = preset

	def output_scene(self, scene, old_scene):
		i = 0
		print("old_scene:", old_scene)
		print("scene:")

		# effects on/off
		while i < NUMBER_OF_EFFECTS:
			val = 0
			if scene.effects[i]:
				val = 127
			msg = [CONTROL_CHANGE | MIDI_EFFECTS_CHANNEL, index_to_cc_map[i], val]
			if not old_scene or old_scene.effects[i] != scene.effects[i]:
				print("out:", msg)
				self.midiout.send_message(msg)
				time.sleep(0.01)
			i += 1

		# volume
		if (not old_scene or old_scene.vol != scene.vol) and scene.vol != -1:
			vol = scene.vol + 20
			msg = [CONTROL_CHANGE | MIDI_EFFECTS_CHANNEL, CC_VOL, vol]
			print("vol:", msg)
			self.midiout.send_message(msg)
			time.sleep(0.01)

		# cc1
		if (not old_scene or old_scene.cc1 != scene.cc1) and scene.cc1 != -1:
			msg = [CONTROL_CHANGE | MIDI_EFFECTS_CHANNEL, CC1, scene.cc1]
			print("cc1:", msg)
			self.midiout.send_message(msg)
			time.sleep(0.01)			

		# cc2
		if (not old_scene or old_scene.cc2 != scene.cc2) and scene.cc2 != -1:
			msg = [CONTROL_CHANGE | MIDI_EFFECTS_CHANNEL, CC2, scene.cc2]
			print("cc2:", msg)
			self.midiout.send_message(msg)
			time.sleep(0.01)

		# External PC (for switching ToneX presets)
		if (not old_scene or old_scene.ext_pc != scene.ext_pc) and scene.ext_pc != -1:
			msg = [PROGRAM_CHANGE | MIDI_EXT_CHANNEL, scene.ext_pc]
			print("pc :", msg)
			self.midiout.send_message(msg)
			time.sleep(0.01)

	def output_effect(self, effect):
		val = 0
		if effect.enabled:
			val = 127
		msg = [CONTROL_CHANGE | MIDI_EFFECTS_CHANNEL, index_to_cc_map[effect.index], val]
		print("out:", msg)
		self.midiout.send_message(msg)
		time.sleep(0.01)

	def output_volume(self, volume):
		vol = volume.value + 20
		msg = [CONTROL_CHANGE | MIDI_EFFECTS_CHANNEL, CC_VOL, vol]
		print("vol:", msg)
		self.midiout.send_message(msg)
		time.sleep(0.01)

	def output_cc(self, cc):
		if cc.value >= 0 and cc.value < 128:
			if cc.id == "cc1":
				msg = [CONTROL_CHANGE | MIDI_EFFECTS_CHANNEL, CC1, cc.value]
			elif cc.id == "cc2":
				msg = [CONTROL_CHANGE | MIDI_EFFECTS_CHANNEL, CC2, cc.value]
			elif cc.id == "ext_cc":
				msg = [CONTROL_CHANGE | MIDI_EXT_CHANNEL, CC_EXT, cc.value]
			print("cc :", msg)
			self.midiout.send_message(msg)
			time.sleep(0.01)

	def output_pc(self, pc):
		if pc.value >= 0 and pc.value < 128:
			msg = None
			if pc.id == "ext_pc":
				msg = [CONTROL_CHANGE | MIDI_EXT_CHANNEL, pc.value]
			if msg:
				print("pc :", msg)
				self.midiout.send_message(msg)
				time.sleep(0.01)

			
					


