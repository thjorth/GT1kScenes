import pygame
import widgets.effectArray

import fonts.fonts

COLOR_COMP = (102, 194, 255)
COLOR_GREEN = (0, 255, 0)
COLOR_DELAY = (3,87,255)
COLOR_CHORUS = (255, 209, 26)
COLOR_DRIVE = (255, 0, 102)

SCENE_TEXT_COLOR = (255, 255, 255)

FONT_SIZE = 450
FONT_SIZE_LABEL = 36

class Preset():
	def __init__(self, screen):
		self.fonts = fonts.fonts.Fonts()

		self.active_scene_index = 0
		#self.font = pygame.font.Font("fonts/NewsflashBB.ttf", FONT_SIZE)
		#self.font_label = pygame.font.Font("fonts/NewsflashBB.ttf", FONT_SIZE_LABEL)

		self.screen = screen
		self.effects = widgets.effectArray.EffectsArray(None)
		comp = widgets.effect.Effect(screen, 0, 0, COLOR_COMP, "Comp")
		self.effects.add(comp)

		drive1 = widgets.effect.Effect(screen, 1, 0, COLOR_DRIVE, "Drive 1")
		self.effects.add(drive1)
		drive2 = widgets.effect.Effect(screen, 2, 0, COLOR_DRIVE, "Drive 2")
		self.effects.add(drive2)

		m_delay = widgets.effect.Effect(screen, 3, 0, COLOR_DELAY, "M Delay")
		self.effects.add(m_delay)
		delay = widgets.effect.Effect(screen, 4, 0, COLOR_DELAY, "Delay")
		self.effects.add(delay)

		chorus = widgets.effect.Effect(screen, 0, 1, COLOR_CHORUS, "Chorus")
		self.effects.add(chorus)

		effect1 = widgets.effect.Effect(screen, 1, 1, COLOR_GREEN, "FX 1")
		self.effects.add(effect1)
		effect2 = widgets.effect.Effect(screen, 2, 1, COLOR_GREEN, "FX 2")
		self.effects.add(effect2)
		effect3 = widgets.effect.Effect(screen, 3, 1, COLOR_GREEN, "FX 3")
		self.effects.add(effect3)
		effect4 = widgets.effect.Effect(screen, 4, 1, COLOR_GREEN, "FX 4")
		self.effects.add(effect4)

	def init_from_scene(self, scene):
		self.effects.init_from_scene(scene)
		self.active_scene_index = scene.index

	def render(self):
		text = self.fonts.scene_label_font.render("Scene:", True, SCENE_TEXT_COLOR)
		self.screen.blit(text, (30, 20))

		scene_no = self.fonts.scene_font.render(str(self.active_scene_index + 1), True, SCENE_TEXT_COLOR)
		self.screen.blit(scene_no, (20, 50))

		self.effects.render()
		
	def set_toggle_callback(self, toggle_callback):
		self.effects.set_toggle_callback(toggle_callback)
	
	def left(self):
		self.effects.left()

	def right(self):
		self.effects.right()

	def up(self):
		self.effects.up()

	def down(self):
		self.effects.down()

	def toggle(self):
		self.effects.toggle()
		