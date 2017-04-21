import pygame, sys

def window_init():
	pygame.init()
	size = width, height = 960, 720
	screen = pygame.display.set_mode(size)
	screen.fill((255,218,185))
	pygame.display.update()

def get_canvas():
	pass

def main():
	window_init()
	while 1:
		for event in pygame.event.get():
			if event.type == pygame.QUIT: sys.exit()

if __name__ == "__main__":
	main()