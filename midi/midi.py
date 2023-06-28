import rtmidi
import singleton

MIDI_DEVICE = "UM-ONE"

class Midi(singleton.SingletonClass):
	def __init__(self):
		# get our MIDI connections set up
		self.midiout_index = -1
		self.midiin_index = -1

		self.midiout = rtmidi.MidiOut()
		available_out_ports = self.midiout.get_ports()
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

		self.midiin = rtmidi.MidiIn()
		available_in_ports = self.midiin.get_ports()
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

	def __del__(self):
		self.midiout.close_port()
		self.midiin.close_port()
		del self.midiout
		del self.midiin

