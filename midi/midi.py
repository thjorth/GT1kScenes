import rtmidi
import time

import mido

mido.set_backend('mido.backends.pygame')
outs = mido.get_output_names()
print("outs: ", outs)

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

class Midi(singleton.SingletonClass):
	def __init__(self):
		self.timer = time.time()
		self.preset = None
		# get our MIDI connections set up
		self.midiout_index = -1
		self.midiin_index = -1

		available_out_ports = mido.get_output_names()
		i = 0
		found = False
		while i < len(available_out_ports) and not found:
			if available_out_ports[i].startswith(MIDI_DEVICE):
				self.midiout_index = i
				print("out: ", available_out_ports[i])
				self.midiout = mido.open_output(available_out_ports[i])
				found = True
			i += 1
		if not found:
			self.midiout = mido.open_output()

		available_in_ports = mido.get_input_names()
		print("ins: ", available_in_ports)
		i = 0
		found = False
		while i < len(available_in_ports) and not found:
			if available_in_ports[i].startswith(MIDI_DEVICE):
				self.midiin_index = i
				print("in:  ", available_in_ports[i])
				self.midiin = mido.open_input(available_in_ports[i])
				found = True
			i += 1
		if not found:
			self.midin = mido.open_input()


	def __del__(self):
		self.midiout.close()
		self.midiin.close()
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
			
			if not old_scene or old_scene.effects[i] != scene.effects[i]:
				self.midiout.send(mido.Message('control_change', channel=MIDI_EFFECTS_CHANNEL, control=index_to_cc_map[i], value=val))
				time.sleep(0.01)
			i += 1

		# volume
		if (not old_scene or old_scene.vol != scene.vol) and scene.vol != -1:
			vol = scene.vol + 20
			msg = mido.Message('control_change', channel=MIDI_EFFECTS_CHANNEL, control=CC_VOL, value=vol)
			self.midiout.send(msg)
			time.sleep(0.01)

		# cc1
		if (not old_scene or old_scene.cc1 != scene.cc1) and scene.cc1 != -1:
			msg = mido.Message('control_change', channel=MIDI_EFFECTS_CHANNEL, control=CC1, value=scene.cc1)
			self.midiout.send(msg)
			time.sleep(0.01)			

		# cc2
		if (not old_scene or old_scene.cc2 != scene.cc2) and scene.cc2 != -1:
			msg = mido.Message('control_change', channel=MIDI_EFFECTS_CHANNEL, control=CC2, value=scene.cc2)
			self.midiout.send(msg)
			time.sleep(0.01)

		# External PC (for switching ToneX presets)
		if (not old_scene or old_scene.ext_pc != scene.ext_pc) and scene.ext_pc != -1:
			msg = mido.Message('program_change', channel=MIDI_EFFECTS_CHANNEL, program=scene.ext_pc)
			self.midiout.send(msg)
			time.sleep(0.01)

	def output_effect(self, effect):
		val = 0
		if effect.enabled:
			val = 127
		msg = mido.Message('control_change', channel=MIDI_EFFECTS_CHANNEL, control=index_to_cc_map[effect.index], value=val)
		self.midiout.send(msg)
		time.sleep(0.01)

	def output_volume(self, volume):
		vol = volume.value + 20
		msg = mido.Message('control_change', channel=MIDI_EFFECTS_CHANNEL, control=CC_VOL, value=vol)
		self.midiout.send(msg)
		time.sleep(0.01)

	def output_cc(self, cc):
		if cc.value >= 0 and cc.value < 128:
			if cc.id == "cc1":
				msg = mido.Message('control_change', channel=MIDI_EFFECTS_CHANNEL, control=CC1, value=cc.value)
			elif cc.id == "cc2":
				msg = mido.Message('control_change', channel=MIDI_EFFECTS_CHANNEL, control=CC2, value=cc.value)
			elif cc.id == "ext_cc":
				msg = mido.Message('control_change', channel=MIDI_EFFECTS_CHANNEL, control=CC_EXT, value=cc.value)

			if msg:
				self.midiout.send(msg)
			time.sleep(0.01)

	def output_pc(self, pc):
		if pc.value >= 0 and pc.value < 128:
			if pc.id == "ext_pc":
				msg = mido.Message('program_change', channel=MIDI_EFFECTS_CHANNEL, program=pc.value)
				self.midiout.send(msg)

			
					


