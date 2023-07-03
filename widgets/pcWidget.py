import pygame
import widgets.effectWidget
import fonts.fonts
PC_MAX = 127
PC_MIN = -1

from constants import (
	SCREEN_WIDTH,
	BUTTON_WIDTH,
	BUTTON_HEIGHT,
	SPACE_BETWEEN,
	FONT_SIZE
)

class PCWidget(widgets.effectWidget.EffectWidget):
	def __init__(self, screen, posx, posy, color, text, id):
		super().__init__(screen, posx, posy, color, text)
		self.value = -1
		self.id = id

	def render(self):
		super().render()
		s = ""
		if self.value < 0:
			s += "---"
		else:
			s += str(self.value)

		text = self.fonts.effect_font.render(s, True, (255,255,255))
		self.screen.blit(text, (self.x + 10, self.y + 46))

	def set_value(self, value):
		self.value = value

	def inc(self):
		if (self.value < PC_MAX):
			self.value += 1

	def dec(self):
		if (self.value > PC_MIN):
			self.value -= 1

	def toggle(self):
		# override that should do nothing
		pass
