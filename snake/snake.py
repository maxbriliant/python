import pygame, sys
from pygame.locals import *
import time
import random
from collections import deque

pygame.init()

WHITE = (255, 255, 255)
GREEN = (0, 150, 0)
RED = (255, 0, 0)

snakeList = deque([])

DISPLAY = pygame.display.set_mode((500, 500), 0, 32)
DISPLAY.fill(WHITE)
pygame.display.update()

class Food():
	xfactor = int(random.randint(0,20))
	yfactor = int(random.randint(0,20))
	
	x = int(500/20 * xfactor )  
	y = int(500/20 * yfactor ) 

	taken = False

	def reset(self):
		self.xfactor = int(random.randint(0,20))
		self.yfactor = int(random.randint(0,20))


		self.x = int(random.randint(0,20))
		self.y = int(random.randint(0,20))
	
		self.x = int(500/20 * self.xfactor )  
		self.y = int(500/20 * self.yfactor ) 

		self.taken = False


class Snake():
	alive = True
	head = pygame.Rect(0, 0, 20, 20)
	direction = None

	x = 0
	y = 0

	headPos = (x, y)

	def grow(self):
		global snakeList
		snakeList.append(Snake())
		snakeList[-1].x = snakeList[-2].x - 25
		snakeList[-1].y = snakeList[-2].y - 25 
		print(snakeList)

def colisionBerry():
	if snake.x + 20 >= berry.x  and snake.x  <= berry.x + 20 and snake.y + 20 >= berry.y and snake.y <= berry.y + 20:
		berry.taken = True
		snake.grow()
		return True

	else:
		return False


snake = Snake()
snakeList.append(snake)
berry = Food()

while True:
	for event in pygame.event.get():
		if event.type == QUIT:
			pygame.quit()
			sys.exit()
	
		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_LEFT:
				snake.direction = "left"
			if event.key == pygame.K_RIGHT:
				snake.direction = "right"
			if event.key == pygame.K_UP:
				snake.direction = "up"
			if event.key == pygame.K_DOWN:
				snake.direction = "down"

	if snake.alive == True:
		if snake.direction == "left":
			snake.x -= 25
		if snake.direction == "right":
			snake.x += 25
		if snake.direction == "up":
			snake.y -= 25
		if snake.direction == "down":
			snake.y += 25

	if berry.taken == False:
		pygame.draw.rect(DISPLAY, RED, (berry.x, berry.y, 20, 20))
		pygame.display.update()
	else:
		pygame.draw.rect(DISPLAY, WHITE, (berry.x, berry.y, 20, 20))
		pygame.display.update()
		berry.reset()

	if colisionBerry() == True:
		berry.taken = True
		berry.reset()



	pygame.time.wait(150)
	DISPLAY.fill(WHITE)
	pygame.draw.rect(DISPLAY, GREEN, (snake.x, snake.y, snake.head.w, snake.head.h))
	
	## draw every item in snakeList
	#for each in snakeList:
	#	pygame.draw.rect(DISPLAY, GREEN, (each.x, each.y, 20, 20))	



	pygame.display.update()