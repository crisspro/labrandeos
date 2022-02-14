class Disco():
	def __init__(self, titulo, autor, fecha, genero, comentarios):
		self.titulo = titulo
		self.autor = autor
		self.fecha = fecha
		self.genero = genero
		self.comentarios = comentarios

	def retornar_datos(self):
		return (self.titulo, self.autor, self.genero, self.ano, self.comentario)