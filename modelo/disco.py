class Disco():
	def __init__(self):
		self.titulo = 'Sin título'
		self.autor = 'Sin autor'
		self.fecha = ''
		self.genero = ''
		self.comentarios = ''

	def retornar_datos(self):
		return (self.titulo, self.autor, self.genero, self.ano, self.comentario)