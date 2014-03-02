# Heeloooo
"""
import tkinter, tkinter.filedialog

options = {}
options['title'] = 'Select Alpha Centari Folder'
directory = tkinter.filedialog.askdirectory(**options)
print(directory)

f = open('options.txt', 'w')
f.write(directory);
"""


import os, sys
import pygame
from pygame.locals import *

pygame.init()

def load_image(name, colorkey=None):
	fullname = os.path.join('data', name)
	try:
		image = pygame.image.load(fullname)
	except pygame.error as message:
		print('Cannot load image:', name)
		raise SystemExit(message)
	image = image.convert()
	if colorkey is not None:
		if colorkey is -1:
			colorkey = image.get_at((0,0))
			image.set_colorkey(colorkey)
	return image, image.get_rect()


fpsClock = pygame.time.Clock();

screen_width=1024
screen_height=768
screen=pygame.display.set_mode([screen_width,screen_height])
#pygame.time.Clock.tick(60) # forces the game to only go 60 fps
alphalocation = "C:/GOG Games/Sid Meier's Alpha Centauri/"
mainmenubackground = load_image(alphalocation + "openinga.pcx", None)

background = mainmenubackground

#pygame.display.set_caption(pygame.time.Clock.get_fps)
screen.blit(background[0], (0, 0))

#open the script!
#ok I believe these are desciptions for menus and various other popups.  I'll pump them into a dict to use them.
#will allow us to use already made translations for the project, etc by using the native format.
scriptdictionary = dict()
with open (os.path.join(alphalocation, "Script.txt")) as script:
	first = True
	for line in script:
		if ";" not in line and len(line) > 0:
			if line[0]=="#":
				key = line[1:]
				print(key)
				
				


while True:
	
	for event in pygame.event.get():
		if event.type == QUIT:
			pygame.quit()
			sys.exit()
		if event.type == KEYDOWN:
			if event.key == K_ESCAPE:
				pygame.event.post(pygame.event.Event(QUIT))

	
	pygame.display.update()
	fpsClock.tick(60)