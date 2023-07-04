import pygame
import time
import models.scene
import models.preset
import midi.midi
import json
import sys

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
preset.select_scene(0)

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
			print(event)
			print(pygame.key.name(event.key))
			match pygame.key.name(event.key):
				case "f1":
					ui_state = STATE_SCENE
					preset.set_ui_state(STATE_SCENE)
				case "f2":
					ui_state = STATE_NAME_EDIT
					preset.set_ui_state(STATE_NAME_EDIT)

			if ui_state == STATE_SCENE:
				match pygame.key.name(event.key):
					case "left":
						preset.left()
					case "right":
						preset.right()
					case "up":
						preset.up()
					case "down":
						preset.down()
					case "space":
						preset.toggle()
					case "page up":
						preset.inc()
					case "page down":
						preset.dec()
					case "1":
						preset.select_scene(0)
					case "2":
						preset.select_scene(1)
					case "3":
						preset.select_scene(2)
					case "4":
						preset.select_scene(3)
					case "5":
						preset.select_scene(4)
					case "6":
						preset.select_scene(5)
					case "s":
						preset.save_presets()

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