import pygame
import time
from threading import *
import random
from pygame.locals import *

KEYS = (K_RIGHT, K_LEFT, K_UP)

class TetrisAgent(Thread):

	def __init__(self):
		Thread.__init__(self)
		self.terminate_flag = 0
		pass

	def get_next_key(self):
		return KEYS[random.randint(0,2)]

	def set_terminate_flag(self):
		self.terminate_flag = True

	def run(self):
		while(not self.terminate_flag):
			pygame.event.post(pygame.event.Event(KEYDOWN, {"key" : K_DOWN}))
			pygame.event.post(pygame.event.Event(KEYDOWN, {"key" : self.get_next_key()}))
			time.sleep(0.05)