import pygame
import widgets.iWidget
import widgets.effectWidget
import widgets.volumeWidget
import widgets.ccWidget
import widgets.pcWidget
import numpy as np

ARRAY_WIDTH = 5
ARRAY_HEIGHT = 3


class EffectsArrayWidget():
	def __init__(self, change_callback):
		self.effects = []
		self.x = 0
		self.y = 0
		self.change_callback = change_callback
		self.volume = None
		self.cc1 = None
		self.cc2 = None
		self.ext_pc = None
		self.ext_cc = None

	def add(self, effect) -> None:
		effect.set_index(len(self.effects))
		self.effects.append(effect)

		if type(effect) is widgets.volumeWidget.VolumeWidget:
			self.volume = effect
		if type(effect) is widgets.ccWidget.CCWidget:
			if effect.id == "cc1":
				self.cc1 = effect
			if effect.id == "cc2":
				self.cc2 = effect
			if effect.id == "ext_cc":
				self.ext_cc = effect
		if type(effect) is widgets.pcWidget.PCWidget:
			self.ext_pc = effect

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
		self.change_callback(self.effects[self.x + self.y * ARRAY_WIDTH])

	def inc(self):
		effect = self.effects[self.x + self.y * ARRAY_WIDTH]
		effect.inc()
		self.change_callback(effect)

	def dec(self):
		effect = self.effects[self.x + self.y * ARRAY_WIDTH]
		effect.dec()
		self.change_callback(effect)

	def inc_volume(self):
		self.volume.inc()
		self.change_callback(self.volume)

	def dec_volume(self):
		self.volume.dec()
		self.change_callback(self.volume)

	def set_selected(self):
		self.reset_selected()
		self.effects[self.x + self.y * ARRAY_WIDTH].select()

	def init_from_scene(self, scene):
		i = 0
		while i < len(self.effects) and i < len(scene.effects):
			self.effects[i].set_enabled(scene.effects[i])
			i += 1
		self.volume.set_volume(scene.vol)
		self.cc1.set_value(scene.cc1)
		self.cc2.set_value(scene.cc2)
		self.ext_cc.set_value(scene.ext_cc)
		self.ext_pc.set_value(scene.ext_pc)

	def set_toggle_callback(self, toggle_callback):
		self.toggle_callback = toggle_callback
	
	def set_volume_callback(self, volume_callback):
		self.volume_callback = volume_callback

	def set_cc_callback(self, cc_callback):
		self.cc_callback = cc_callback
