class Data():
	def __init__(self, *ARGS, **KWARGS):
		self.titulo= 'Sin título'
		self.autor= 'Sin autor'
		self.tiempo_inicio = 0
		
		# lista de  marcas.
		self.lista_marcas= []
	
	# añade una nueva marca a la lista.
	def agregarMarca(self, marca):
		self.lista_marcas.append(marca)


	# limpia la lista de marcas.
	def limpiar (self):
		self.lista_marcas.clear()


class Marca():
	def __init__(self, titulo, autor, tiempo_inicio):
		self.titulo = titulo
		self.autor = autor
		self.inicio = tiempo_inicio

	def __str__(self):
		return "{titulo} ({autor})".format(titulo=self.titulo, autor=self.autor)


