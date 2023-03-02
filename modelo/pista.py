class Pista():
	def __init__(self, nombre, extension, direccion, ruta, duracion):
		self.nombre = nombre
		self.extension = extension
		self.direccion = direccion
		self.ruta = ruta
		self.duracion = duracion
		self.taza_bit = ''
		self.modo_taza_bit = ''
		self.velocidad_muestreo = ''
		self.canales = 2

	def __eq__(self, otro):
		if isinstance(otro, Pista):
			return vars(self) == vars(otro)
