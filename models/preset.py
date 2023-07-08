from models.scene import Scene
import widgets.effectArrayWidget
import widgets.effectWidget
import widgets.volumeWidget
import widgets.ccWidget
import widgets.pcWidget
from data.presetsFile import PresetsFile
import pygame

STATE_SCENE = 1
STATE_NAME_EDIT = 2

import fonts.fonts

NUMBER_OF_SCENES = 6
SEPARATOR = "::"

BACKGROUND_COLOR = (0, 0, 0)

COLOR_COMP = (102, 194, 255)
COLOR_GREEN = (0, 255, 0)
COLOR_DELAY = (3,87,255)
COLOR_CHORUS = (255, 209, 26)
COLOR_DRIVE = (255, 0, 102)
COLOR_CC = (255, 255, 255)

SCENE_TEXT_COLOR = (255, 255, 255)

FONT_SIZE = 450
FONT_SIZE_LABEL = 36

class Preset():
	def __init__(self, midi, screen):
		self.fonts = fonts.fonts.Fonts()
		self.active_scene_index = 0
		self.screen = screen
		self.ui_state = STATE_SCENE

		self.copy_buffer = None

		self.effects_widget = widgets.effectArrayWidget.EffectsArrayWidget(self.on_change_callback)

		comp = widgets.effectWidget.EffectWidget(screen, 0, 0, COLOR_COMP, "Comp")
		self.effects_widget.add(comp)

		drive1 = widgets.effectWidget.EffectWidget(screen, 1, 0, COLOR_DRIVE, "Drive 1")
		self.effects_widget.add(drive1)
		drive2 = widgets.effectWidget.EffectWidget(screen, 2, 0, COLOR_DRIVE, "Drive 2")
		self.effects_widget.add(drive2)

		m_delay = widgets.effectWidget.EffectWidget(screen, 3, 0, COLOR_DELAY, "M Delay")
		self.effects_widget.add(m_delay)
		delay = widgets.effectWidget.EffectWidget(screen, 4, 0, COLOR_DELAY, "Delay")
		self.effects_widget.add(delay)

		chorus = widgets.effectWidget.EffectWidget(screen, 0, 1, COLOR_CHORUS, "Chorus")
		self.effects_widget.add(chorus)

		effect1 = widgets.effectWidget.EffectWidget(screen, 1, 1, COLOR_GREEN, "FX 1")
		self.effects_widget.add(effect1)
		effect2 = widgets.effectWidget.EffectWidget(screen, 2, 1, COLOR_GREEN, "FX 2")
		self.effects_widget.add(effect2)
		effect3 = widgets.effectWidget.EffectWidget(screen, 3, 1, COLOR_GREEN, "FX 3")
		self.effects_widget.add(effect3)
		effect4 = widgets.effectWidget.EffectWidget(screen, 4, 1, COLOR_GREEN, "FX 4")
		self.effects_widget.add(effect4)

		volume = widgets.volumeWidget.VolumeWidget(screen, 0, 2, COLOR_CC, "Volume")
		self.effects_widget.add(volume)

		cc1 = widgets.ccWidget.CCWidget(screen, 1, 2, COLOR_CC, "CC 1", "cc1")
		self.effects_widget.add(cc1)
		cc2 = widgets.ccWidget.CCWidget(screen, 2, 2, COLOR_CC, "CC 2", "cc2")
		self.effects_widget.add(cc2)

		ext_pc = widgets.pcWidget.PCWidget(screen, 3, 2, COLOR_CC, "Ext PC", "ext_pc")
		self.effects_widget.add(ext_pc)

		ext_cc = widgets.ccWidget.CCWidget(screen, 4, 2, COLOR_CC, "Ext CC", "ext_cc")
		self.effects_widget.add(ext_cc)

		self.name = ""

		self.presets_file = PresetsFile()

		self.midi = midi
		midi.set_preset(self)
		self.reset()

	def select_preset(self, index):
		self.presets_file.select_preset(index)
		self.reset()

	def reset(self):
		self.old_scene = None
		
		self.scenes = (
			Scene(0),
			Scene(1),
			Scene(2),
			Scene(3),
			Scene(4),
			Scene(5),
		)
		self.index = 0
		self.active_scene = None
		self.deserialize(self.presets_file.get_active_preset())
		self.load_scene()

 
	def update_preset(self):
		self.presets_file.update_active_preset(self.serialize())

	def load_scene(self):
		self.active_scene = self.scenes[self.index]
		self.init_from_scene(self.active_scene)
		self.render()

	def init_from_scene(self, scene):
		self.effects_widget.init_from_scene(scene)
		self.active_scene_index = scene.index

	def set_ui_state(self, ui_state):
		self.ui_state = ui_state
		self.update_preset()
		self.render()

	def render(self):
		self.screen.fill(BACKGROUND_COLOR)
		if self.ui_state == STATE_SCENE:
			self.render_scene()
		elif self.ui_state == STATE_NAME_EDIT:
			self.render_name_editor()
		pygame.display.flip()
		
		

	def render_name_editor(self):
		# implement
		text = self.fonts.scene_label_font.render("Name:", True, SCENE_TEXT_COLOR)
		self.screen.blit(text, (30, 20))

		name = self.name.replace("\n", "") + "_"
		text = self.fonts.edit_font.render(name, True, SCENE_TEXT_COLOR)
		self.screen.blit(text, (30, 80))

	def render_scene(self):
		text = self.fonts.scene_label_font.render("Scene:", True, SCENE_TEXT_COLOR)
		self.screen.blit(text, (30, 20))

		preset_str = "#" + str(self.presets_file.active_preset_index + 1)
		name = self.name.replace("\n", "")
		if name != "":
			preset_str += "   " + name
		text = self.fonts.scene_label_font.render(preset_str, True, SCENE_TEXT_COLOR)
		self.screen.blit(text, (240, 20))

		scene_no = self.fonts.scene_font.render(str(self.active_scene_index + 1), True, SCENE_TEXT_COLOR)
		self.screen.blit(scene_no, (20, 50))

		self.effects_widget.render()


	def toggle_callback(self, effect):
		self.active_scene.update_effect(effect.index, effect.enabled)
		self.midi.output_effect(effect)

	def volume_callback(self, volume):
		self.active_scene.update_volume(volume)
		self.midi.output_volume(volume)

	def cc_callback(self, cc):
		self.active_scene.update_cc(cc)
		self.midi.output_cc(cc)

	def on_change_callback(self, effect):
		if type(effect) is widgets.effectWidget.EffectWidget:
			self.active_scene.update_effect(effect.index, effect.enabled)
			self.midi.output_effect(effect)
		elif type(effect) is widgets.volumeWidget.VolumeWidget:
			self.active_scene.update_volume(effect)
			self.midi.output_volume(effect)
		elif type(effect) is widgets.ccWidget.CCWidget:
			self.active_scene.update_cc(effect)
			self.midi.output_cc(effect)
		elif type(effect) is widgets.pcWidget.PCWidget:
			self.active_scene.update_pc(effect)
			self.midi.output_pc(effect)

		self.update_preset()		


	def select_scene(self, index):
		print("selecting scene:", index)
		print("self:", self)
		if index >= 0 and index < len(self.scenes):
			self.index = index
			self.load_scene()
			self.midi.output_scene(self.active_scene, self.old_scene)
			self.old_scene = self.active_scene

	def save_presets(self):
		self.presets_file.save()

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

	def left(self):
		self.effects_widget.left()

	def right(self):
		self.effects_widget.right()

	def up(self):
		self.effects_widget.up()

	def down(self):
		self.effects_widget.down()

	def toggle(self):
		self.effects_widget.toggle()

	def inc(self):
		self.effects_widget.inc()

	def dec(self):
		self.effects_widget.dec()

	def edit_backspace(self):
		name = self.name.replace("\n", "")
		if len(name) > 0:
			name = name[:-1]
		self.name = name + "\n"

		self.update_preset()

	def edit_add_char(self, char):
		name = self.name.replace("\n", "")
		name += char
		self.name = name + "\n"
	
	def edit_save(self):
		self.update_preset()

	def copy_scene(self):
		self.copy_buffer = self.active_scene.serialize()

	def paste_scene(self):
		if self.copy_buffer:
			old_scene = Scene(self.active_scene)
			old_scene.deserialize(self.active_scene.serialize())
			self.old_scene = old_scene
			self.active_scene.deserialize(self.copy_buffer)
			self.update_preset()
			self.select_scene(self.active_scene_index)
		