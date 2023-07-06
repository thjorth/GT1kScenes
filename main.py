import pygame
import time
import models.scene
import models.preset
import midi.midi
import json
import sys
import mido

mido.set_backend('mido.backends.pygame')
outs = mido.get_output_names()
print("outs: ", outs)

WIN_WIDTH = 800
WIN_HEIGHT = 480

STATE_SCENE = 1
STATE_NAME_EDIT = 2

ui_state = STATE_SCENE

pygame.init()
pygame.font.init()

background_colour = (0, 0, 0)

window_style = 0
if "--fullscreen" in sys.argv:
	window_style = pygame.FULLSCREEN

screen = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT), window_style)
pygame.display.set_caption('GT-1000 Scenes')
screen.fill(background_colour)

pygame.display.flip()

running = True

def render():
	screen.fill(background_colour)
	preset.render()

	pygame.display.flip()

midi = midi.midi.Midi()
preset = models.preset.Preset(midi, screen)
active_preset = 0
preset.select_scene(active_preset)

render()

while running:
	# midi stuff first
	if midi.respond():
		render()

	for event in pygame.event.get():
	  
		# Check for QUIT event      
		if event.type == pygame.QUIT:
			running = False

		if event.type == pygame.KEYDOWN:
			print(pygame.key.name(event.key))
			key_name = pygame.key.name(event.key)
			if key_name == "f1":
				ui_state = STATE_SCENE
				preset.set_ui_state(STATE_SCENE)
			elif key_name == "f2":
				ui_state = STATE_NAME_EDIT
				preset.set_ui_state(STATE_NAME_EDIT)
			elif key_name == "q":
				keys = pygame.key.get_pressed()
				if keys[pygame.K_LCTRL]:
					running = False
				
			if ui_state == STATE_SCENE:
				if key_name == "left":
					preset.left()
				elif key_name == "right":
					preset.right()
				elif key_name == "up":
					preset.up()
				elif key_name == "down":
					preset.down()
				elif key_name == "space":
					preset.toggle()
				elif key_name == "page up":
					preset.inc()
				elif key_name == "page down":
					preset.dec()
				elif key_name == "1":
					preset.select_scene(0)
				elif key_name == "2":
					preset.select_scene(1)
				elif key_name == "3":
					preset.select_scene(2)
				elif key_name == "4":
					preset.select_scene(3)
				elif key_name == "5":
					preset.select_scene(4)
				elif key_name == "6":
					preset.select_scene(5)
				elif key_name == "f12":
					preset.save_presets()
				elif key_name == "[+]":
					if active_preset < 249:
						active_preset += 1
						preset.select_preset(active_preset)
				elif key_name == "[-]":
					if active_preset > 0:
						active_preset -= 1
						preset.select_preset(active_preset)
				elif key_name == "c":
					keys = pygame.key.get_pressed()
					if keys[pygame.K_LCTRL]:
						preset.copy_scene()
				elif key_name == "v":
					keys = pygame.key.get_pressed()
					if keys[pygame.K_LCTRL]:
						preset.paste_scene()

			if ui_state == STATE_NAME_EDIT:
				key_name = pygame.key.name(event.key)
				if key_name == "backspace":
					preset.edit_backspace()
				elif key_name == "return":
					preset.edit_save()
					ui_state = STATE_SCENE
					preset.set_ui_state(STATE_SCENE)
				elif event.key >= 32 and event.key <= 126:
					preset.edit_add_char(event.unicode)


			render()
	
	time.sleep(0.01)

preset.save_presets()		
			
del midi