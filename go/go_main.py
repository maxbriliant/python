#!/usr/bin/python3
import pygame, sys
from pygame.locals import *
import numpy as np
import time

SCREEN_X=520
SCREEN_Y=520

stone_rect_x=0  
stone_rect_y=0

stone_len_x=38
stone_len_y=38

white = pygame.image.load('white.png')
white = pygame.transform.scale(white, (38, 38))
black = pygame.image.load('black.png')
black = pygame.transform.scale(black, (38, 38))

stoneList = []





class Stone(object):
	def __init__(self, x, y, c):
		self.x = x
		self.y = y
		self.c = c


class Goban(object):
	def __init__(self):
		self.size = 13
		self.px = 520
		self.lines = 'goban.png'
		self.wood = 'wood.jpeg'
		self.x = self.size
		self.y = self.size
		self.grid = [[0 for i in range(self.x)] for j in range(self.y)]
		#self.grid = self.grid.reverse
		
	
		self.last_placed = (0, 0, '0')



	def is_placed(self, x, y):
		if self.grid[x][y] == 0:
			return False
		else:
			return True
	

	def where_to_place(self, x, y):
		new_x = 520-39*x +21 -18  
		new_y = 520-39*y -21 +18
		return(new_x, new_y)



	def make_stone(self, x, y, c):
		self.grid[x][y] = c
		self.last_placed = (x, y ,c)
		new_x, new_y = self.where_to_place(x, y)
		## debugging
		print(c + ' Stone placed at ' + str(new_x) +', ' + str(new_y))
		## line
		new_stone = Stone(new_x, new_y, c)
		stoneList.append(new_stone)
		return new_stone

	def draw_Stone(self, x, y, c):
		stone = self.make_stone(x-1, y-1, c)
		print (stone.x)
		if stone.c == ('B' or 'b'):
			#black.set_clip(pygame.Rect(stone_rect_x, stone_rect_y, stone_len_x, stone_len_y))
			stone_to_draw = black.subsurface(black.get_clip()) #Extract the sprite you want
		elif stone.c == ('W' or 'w'):
			#white.set_clip(pygame.Rect(stone_rect_x, stone_rect_y, stone_len_x, stone_len_y))
			stone_to_draw = white.subsurface(white.get_clip()) #Extract the sprite you want		
			

def main():
	
	## Goban Object and Grid
	board = Goban()
	board.draw_Stone(1,1, 'W')
	print(*board.grid, sep='\n')




	# Pygame init	
	pygame.init()	
	SCREEN = pygame.display.set_mode((board.px, board.px))
	pygame.display.set_caption('Python Goban')

	layer1 = pygame.image.load(board.wood)
	layer2 = pygame.image.load(board.lines)

	
	white = pygame.image.load('white.png')
	white = pygame.transform.scale(white, (38, 38))
	black = pygame.image.load('black.png')
	black = pygame.transform.scale(black, (38, 38))
	current_color = black

	blit_list 			= [(layer1,(0,0)),(layer2,(0,0))]
	blit_img_list		= [layer1, layer2]
	blit_x_coords 		= [0,0]
	blit_y_coords 		= [0,0]

	while True:
		for event in pygame.event.get():

			for i in range(len(blit_img_list)):
				if(blit_img_list[i] != layer1 or layer2):
					print (blit_img_list[i])
				#if blit_img_list[i].get_rect().collidepoint(pygame.mouse.get_pos()):




			if event.type == pygame.MOUSEBUTTONUP:
				if event.button == 1:	
					pos = pygame.mouse.get_pos()
					pos_x = pos[0]-19
					pos_y = pos[1]-19
					print (str(current_color))
					

					
					blit_img_list.append(current_color)
					blit_x_coords.append(pos_x)
					blit_y_coords.append(pos_y)

					if (current_color == white):
						current_color = black
					else:
						current_color = white
				
				#elif event.button == 3:
						
				#	if blit_img_list[-1] != (layer2):
						#blit_img_list.pop()
						#blit_y_coords.pop()
						#blit_x_coords.pop()
						#if (current_color == white):
						#	current_color = black
						#else:
						#	current_color = white
						#time.sleep(0.2)
						
			if event.type == QUIT:
				pygame.quit()
				sys.exit()


			# SCREEN.blit(black, board.where_to_place(11,11))
			# SCREEN.blit(black, board.where_to_place(4,4))
			# SCREEN.blit(black, board.where_to_place(4,11))
			# SCREEN.blit(black, board.where_to_place(11,4))
			# SCREEN.blit(black, board.where_to_place(7,7))
			# SCREEN.blit(white, board.where_to_place(13,13))
			# SCREEN.blit(white, board.where_to_place(1,1))
			# SCREEN.blit(white, board.where_to_place(13,1))
			# SCREEN.blit(white, board.where_to_place(1,13))

			for i in range(len(blit_img_list)):
				SCREEN.blit(blit_img_list[i], (blit_x_coords[i], blit_y_coords[i]))
			pygame.display.update()

		#pygame.display.update()
		#draw_Stone(1, 1, 'W')


	
	


if __name__ == '__main__':
		main()



