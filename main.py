import pygame, sys


def window_init():
	pygame.init()
	size = width, height = 960, 720
	can = pygame.display.set_mode(size)
	can.fill((255,218,185))
	pygame.display.update()
	return can

def main():
	main_can = window_init()
	rect = pygame.Surface((200,250))
	rect.fill((0,0,200))
	r = rect.get_rect()
	speed = [1,1]
	while 1:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				sys.exit()
			"""elif(event.type == pygame.KEYDOWN):
				if (event.)
			"""
		r.move_ip(speed)
		main_can.fill((255,218,185))
		main_can.blit(rect, r)
		pygame.time.delay(200)
		pygame.display.update()

if __name__ == "__main__":
	main()