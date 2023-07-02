import pygame
import widgets.volume

COLOR_CC = (255, 255, 255)

class ControlArray():
	def __init__(self):
		self.controls = []
		
	def add(self, control):
		self.controls.append(control)

	def init_from_scene(self, scene):
		# todo
		pass

	def render(self):
		for control in self.controls:
			control.render()
