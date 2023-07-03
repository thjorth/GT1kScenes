import pygame
import time
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
	preset.render()
	pygame.display.flip()

midi = midi.midi.Midi()
preset = models.preset.Preset(midi, screen)
preset.deserialize("0100000000 0 -1 -1 4 -1::0010101000 -6 -1 -1 4 -1::0100011000 4 -1 -1 5 -1::0000000000 0 -1 -1 4 -1::0000000000 0 -1 -1 4 -1::0000000000 0 -1 -1 4 -1::")
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
			print(pygame.key.name(event.key))
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
					print(json.dumps(preset))

			render()
	
	time.sleep(0.01)
		
print(preset.serialize())
			
del midi