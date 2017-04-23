
class Piece:

	def __init__(self, shape, rotation, x, y, color):
		self.shape = shape
		self.rotation = rotation
		self.x = x
		self.y = y
		self.color = color

	def get_shape(self):
		return self.shape

	def get_rotation(self):
		return self.rotation

	def get_x(self):
		return self.x

	def get_y(self):
		return self.y

	def get_color(self):
		return self.color

	def move_left(self):
		self.x = self.x - 1

	def move_right(self):
		self.x = self.x + 1

	def rotate(self, rotation):
		self.rotation = rotation

	def move_down(self, delta=1):
		self.y = self.y + delta

