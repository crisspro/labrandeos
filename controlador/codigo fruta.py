class Fruta():
	def __init__(self, nombre, color=None):
		self.nombre = nombre
		if color is not None:
			self.color = color

f = Fruta("Manzana", "roja")
print(f.__dic__)