class Disco():
	def __init__(self):
		self.titulo = 'Sin título'
		self.autor = 'Sin autor'
		self.genero = ''
		self.ano = ''
		self.comentario = ''

	def retornar_datos(self):
		return (self.titulo, self. autor, self.genero, self.ano, self.comentario)