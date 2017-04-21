import pygame, sys
pygame.init()
size = width, height = 960, 720
screen = pygame.display.set_mode(size)
screen.fill((255,218,185))
pygame.display.update()
def main():
	while 1:
		for event in pygame.event.get():
			if event.type == pygame.QUIT: sys.exit()

if __name__ == "__main__":
	main()