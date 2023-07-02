import pygame
import time
import widgets.effect
import widgets.effectArray
import widgets.preset
import models.scene
import models.preset
import midi.midi
import json

WIN_WIDTH = 800
WIN_HEIGHT = 480

pygame.init()
pygame.font.init()

background_colour = (0, 0, 0)
screen = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
pygame.display.set_caption('GT-1000 Scenes')
screen.fill(background_colour)

pygame.display.flip()

running = True

def render():
	screen.fill(background_colour)
	preset_widget.render()
	pygame.display.flip()

midi = midi.midi.Midi()
preset_widget = widgets.preset.Preset(screen)
preset = models.preset.Preset(preset_widget, midi)
preset.deserialize("0100000000 0 -1 -1 4 -1::0010101000 -6 -1 -1 4 -1::0100011000 4 -1 -1 5 -1::0000000000 0 -1 -1 4 -1::0000000000 0 -1 -1 4 -1::0000000000 0 -1 -1 4 -1::")
preset.select_scene(0)
preset_widget.render()

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
			match pygame.key.name(event.key):
				case "left":
					preset_widget.left()
				case "right":
					preset_widget.right()
				case "up":
					preset_widget.up()
				case "down":
					preset_widget.down()
				case "space":
					preset_widget.toggle()
				case "page up":
					preset_widget.inc()
				case "page down":
					preset_widget.dec()
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
					print(json.dumps(preset))

			render()
	
	time.sleep(0.01)
		
print(preset.serialize())
			
del midi