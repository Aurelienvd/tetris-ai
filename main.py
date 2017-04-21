import pygame, sys
from pygame.locals import *

def window_init():
	pygame.init()
	size = width, height = 960, 720
	can = pygame.display.set_mode(size)
	can.fill((255,218,185))
	pygame.display.update()
	pygame.key.set_repeat(10, 50)
	return can

def main():
	main_can = window_init()
	rect = pygame.Surface((200,250))
	rect.fill((0,0,200))
	main_can.blit(rect, (0,0))
	x = 0
	y = 0
	while 1:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				sys.exit()
			elif(event.type == pygame.KEYDOWN):
				if (event.key == K_RIGHT):
					x = x + 10
				if (event.key == K_LEFT):
					x = x - 10
				if (event.key == K_UP):
					y = y - 10
				if (event.key == K_DOWN):
					y = y + 10
		main_can.fill((255,218,185))
		main_can.blit(rect, (x,y))
		pygame.time.delay(10)
		pygame.display.update()

if __name__ == "__main__":
	main()