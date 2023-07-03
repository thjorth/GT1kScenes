import pygame
import widgets.iWidget
import fonts.fonts

from constants import (
    SCREEN_WIDTH,
    BUTTON_WIDTH,
    BUTTON_HEIGHT,
    SPACE_BETWEEN,
    FONT_SIZE
)

OFFSET_X = 200
OFFSET_Y = -4

OFFSET_X = SCREEN_WIDTH - 5 * (BUTTON_WIDTH + SPACE_BETWEEN) - 20

class EffectWidget(widgets.iWidget.IWidget):
	def __init__(self, screen, posx, posy, color, text) -> None:
		self.screen = screen
		self.x = posx * BUTTON_WIDTH + SPACE_BETWEEN + posx * SPACE_BETWEEN + OFFSET_X
		self.y = posy * BUTTON_HEIGHT + SPACE_BETWEEN + posy * SPACE_BETWEEN + OFFSET_Y
		self.color = color
		self.fonts = fonts.fonts.Fonts()
		self.text = text
		self.enabled = False
		self.selected = False
		self.index = 0

	def render(self) -> None:
		width = 6
		text_color = self.color
		if self.enabled:
			width = 0
			text_color = (255,255,255)
			
		if self.selected:
			selected_color = (255,255,255)
		else:
			selected_color = (0,0,0)

		pygame.draw.rect(self.screen, selected_color, pygame.Rect(self.x - 10, self.y - 10, BUTTON_WIDTH + 20, BUTTON_HEIGHT + 20), 12, 15)
		pygame.draw.rect(self.screen, self.color, pygame.Rect(self.x, self.y, BUTTON_WIDTH, BUTTON_HEIGHT), width, 10)
		text = self.fonts.effect_font.render(self.text, True, text_color)
		self.screen.blit(text, (self.x + 10, self.y + 10))

	def deselect(self) -> None:
		self.selected = False

	def disable(self) -> None:
		self.enabled = False
	
	def enable(self) -> None:
		self.enabled = True

	def set_enabled(self, status) -> None:
		self.enabled = status

	def toggle(self) -> None:
		self.enabled = not self.enabled

	def select(self) -> None:
		self.selected = True

	def set_index(self, index):
		self.index = index

	def inc(self):
		""" stub """
		pass
		
	def dec(self):
		""" stub """
		pass
		