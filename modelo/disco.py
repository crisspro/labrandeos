class Disco():
	def __init__(self):
		self.titulo = ''
		self.autor = ''
		self.fecha = ''
		self.genero = ''
		self.comentarios = ''

	def retornar_datos(self):
		return (self.titulo, self.autor, self.genero, self.ano, self.comentario)

	def limpiar(self):
		self.titulo = 'Sin título'
		self.autor = 'Sin autor'
		self.genero = ''
		self.fecha = ''
		self.comentarios = ''

	def __eq__(self, otro):
		if isinstance(otro, Disco):
			return vars(self) == vars(otro)