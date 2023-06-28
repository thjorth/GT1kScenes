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

midi = midi.midi.Midi()

pygame.init()
pygame.font.init()

background_colour = (0, 0, 0)
screen = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
pygame.display.set_caption('Geeksforgeeks')
screen.fill(background_colour)

preset_widget = widgets.preset.Preset(screen)
preset = models.preset.Preset(preset_widget)
preset_widget.render()

pygame.display.flip()

running = True

def render():
	screen.fill(background_colour)
	preset_widget.render()
	pygame.display.flip()

timer = time.time()

while running:
	# midi stuff first

	msg = midi.midiin.get_message()
	if msg:
		message, deltatime = msg
		timer += deltatime
		print("@%0.6f %r" % (timer, message))
		# now write these messages to the midi out to allow midi to pass through
		midi.midiout.send_message(message)

	for event in pygame.event.get():
	  
		# Check for QUIT event      
		if event.type == pygame.QUIT:
			running = False

		if event.type == pygame.KEYDOWN:
			#print(pygame.key.name(event.key)
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
		
			
del midi