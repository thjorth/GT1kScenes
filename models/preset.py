import models.scene

class Preset():
	def __init__(self, effects_widget):
		self.effects_widget = effects_widget
		self.effects_widget.set_toggle_callback(self.toggle_callback)

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

	def select_scene(self, index):
		if index >= 0 and index < len(self.scenes):
			self.index = index
			self.load_scene()
	
		
		