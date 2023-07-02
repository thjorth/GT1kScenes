import pygame
import widgets.iWidget
import widgets.effect
import widgets.volume
import widgets.cc
import widgets.noop
import numpy as np

ARRAY_WIDTH = 5
ARRAY_HEIGHT = 3


class EffectsArray():
	def __init__(self, toggle_callback):
		self.effects = []
		self.x = 0
		self.y = 0
		self.toggle_callback = toggle_callback
		self.volume_callback = None
		self.cc_callback = None
		self.has_focus = True

		self.volume = None
		self.cc1 = None

	def add(self, effect) -> None:
		effect.set_index(len(self.effects))
		self.effects.append(effect)

	def add_volume(self,volume):
		self.add(volume)
		self.volume = volume

	def render(self) -> None:
		self.set_selected()
		for effect in self.effects:
			effect.render()
			
	def reset_selected(self) -> None:
		for effect in self.effects:
			effect.deselect()

	def left(self):
		if self.x > 0:
			self.x -= 1
	
	def right(self):
		self.x += 1
		if self.x >= ARRAY_WIDTH:
			self.x = ARRAY_WIDTH - 1;
	
	def up(self):
		if self.y > 0:
			self.y -= 1

	def down(self):
		self.y += 1
		if (self.y >= ARRAY_HEIGHT):
			self.y = ARRAY_HEIGHT - 1

	def toggle(self):
		self.effects[self.x + self.y * ARRAY_WIDTH].toggle()
		self.toggle_callback(self.effects[self.x + self.y * ARRAY_WIDTH])

	def inc(self):
		effect = self.effects[self.x + self.y * ARRAY_WIDTH]
		effect.inc()
		if (type(effect) is widgets.volume.Volume):
			self.volume_callback(effect)
		if (type(effect) is widgets.cc.CC):
			self.cc_callback(effect)

	def dec(self):
		effect = self.effects[self.x + self.y * ARRAY_WIDTH]
		effect.dec()
		if (type(effect) is widgets.volume.Volume):
			self.volume_callback(effect)
		if (type(effect) is widgets.cc.CC):
			self.cc_callback(effect)
	
	def set_selected(self):
		self.reset_selected()
		self.effects[self.x + self.y * ARRAY_WIDTH].select()

	def init_from_scene(self, scene):
		i = 0
		while i < len(self.effects) and i < len(scene.effects):
			self.effects[i].set_enabled(scene.effects[i])
			i += 1
		self.volume.set_volume(scene.vol)

	def set_toggle_callback(self, toggle_callback):
		self.toggle_callback = toggle_callback
	
	def set_volume_callback(self, volume_callback):
		self.volume_callback = volume_callback

	def set_cc_callback(self, cc_callback):
		self.cc_callback = cc_callback
