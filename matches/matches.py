import pygame, sys
from pygame.locals import *
import time
import random
import os

path = "/home/mx/Programming/Python/matches"

if not os.path.exists('/home/mx/Programming/Python/matches/counter.txt'):
	os.mknod("counter.txt")

with open('counter.txt') as f:
	lines = f.readlines()

pygame.init()
pygame.font.init()
pygame.mixer.init()

sound = pygame.mixer.Sound("match.wav")

countString = lines[0]
countString = countString[0:-1]
global COUNTER
COUNTER = int(countString)

DISPLAY = pygame.display.set_mode((450,350), 0, 32)

BLUE = (0, 0, 255)

timerFont = pygame.font.SysFont('DejaVu Sans', 30)
timer = timerFont.render('count', False, (255,0,0))

boxImg = pygame.image.load("matches.png")
burningImg = pygame.image.load("burning.png")
burningImg = pygame.transform.scale(burningImg, (350,350) )

DISPLAY.fill(BLUE)
DISPLAY.blit(boxImg, (0,0))
pygame.display.update()


while True:
	for event in pygame.event.get():
		if event.type == QUIT:
			
			text_file = open("counter.txt", "w")
			text_file.write(str(COUNTER) + "\n")
			text_file.close()

			pygame.quit()
			sys.exit()
		if event.type == pygame.MOUSEBUTTONUP:
			if COUNTER <= 0:
				DISPLAY.fill(BLUE)
				DISPLAY.blit(boxImg, (0,0))
				pygame.display.update()
			else:
				COUNTER -=1
				sound.play()
				DISPLAY.fill(BLUE)
				DISPLAY.blit(burningImg, (50,0))
				timer = timerFont.render(str(COUNTER), False, (255,220,0))
				DISPLAY.blit(timer, (10,0))
				pygame.display.update()
				pygame.time.wait(2000)
				DISPLAY.fill(BLUE)
				DISPLAY.blit(boxImg, (0,0))
				pygame.display.update()
			