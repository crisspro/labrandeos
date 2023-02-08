class Pista():
	def __init__(self, nombre, extencion, direccion, ruta, duracion):
		self.nombre = nombre
		self.extencion = extencion
		self.direccion = direccion
		self.ruta = ruta
		self.duracion = duracion

	def __eq__(self, otro):
		if isinstance(otro, Pista):
			return vars(self) == vars(otro)
