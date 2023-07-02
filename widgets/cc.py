import pygame
import widgets.effect
import fonts.fonts
CC_MAX = 127
CC_MIN = -1

from constants import (
	SCREEN_WIDTH,
	BUTTON_WIDTH,
	BUTTON_HEIGHT,
	SPACE_BETWEEN,
	FONT_SIZE
)

class CC(widgets.effect.Effect):
	def __init__(self, screen, posx, posy, color, text):
		super().__init__(screen, posx, posy, color, text)
		self.value = -1

	def render(self):
		super().render()
		s = ""
		if self.value < 0:
			s += "-"
		elif (self.value > 0):
			s += "+"
		else:
			s += " "
		s += str(self.value)

		text = self.fonts.effect_font.render(s, True, (255,255,255))
		self.screen.blit(text, (self.x + 10, self.y + 46))

	def set_volume(self, value):
		self.value = value

	def inc(self):
		if (self.value < CC_MAX):
			self.value += 1

	def dec(self):
		if (self.value > CC_MIN):
			self.value -= 1

	def toggle(self):
		# override that should do nothing
		pass
