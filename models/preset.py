import models.scene

NUMBER_OF_SCENES = 6
SEPARATOR = "::"
class Preset():
	def __init__(self, effects_widget, midi):
		self.effects_widget = effects_widget
		self.effects_widget.set_toggle_callback(self.toggle_callback)
		self.effects_widget.set_volume_callback(self.volume_callback)
		self.effects_widget.set_cc_callback(self.cc_callback)
		self.midi = midi
		self.old_scene = None
		self.name = ""
		midi.set_preset(self)
		
		self.scenes = (
			models.scene.Scene(0),
			models.scene.Scene(1),
			models.scene.Scene(2),
			models.scene.Scene(3),
			models.scene.Scene(4),
			models.scene.Scene(5),
		)
		self.index = 0
		self.active_scene = None
		self.load_scene()
		
	def load_scene(self):
		self.active_scene = self.scenes[self.index]
		self.effects_widget.init_from_scene(self.active_scene)

	def toggle_callback(self, effect):
		self.active_scene.update_effect(effect.index, effect.enabled)
		self.midi.output_effect(effect)

	def volume_callback(self, volume):
		self.active_scene.update_volume(volume)
		self.midi.output_volume(volume)

	def cc_callback(self, cc):
		self.active_scene.update_cc(cc)
		self.midi.output_cc(cc)

	def select_scene(self, index):
		if index >= 0 and index < len(self.scenes):
			self.index = index
			self.load_scene()
			self.midi.output_scene(self.active_scene, self.old_scene)
			self.old_scene = self.active_scene

	def serialize(self):
		s = ""
		for scene in self.scenes:
			s += scene.serialize() + SEPARATOR
		s += self.name
		return s
	
	def deserialize(self, s):
		self.old_scene = None
		scene_strs = s.split(SEPARATOR)
		i = 0
		while i < NUMBER_OF_SCENES and i < len(scene_strs) and i < len(self.scenes):
			self.scenes[i].deserialize(scene_strs[i])
			i += 1
		self.name = scene_strs[len(scene_strs) - 1]

		