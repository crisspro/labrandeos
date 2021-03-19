class Data():
	def __init__(self, *ARGS, **KWARGS):
		self.titulo= 'Sin título'
		self.autor= 'Sin autor'
		self.tiempo_inicio = 0

# lista con diccionarios para guardar datos de marcas.
		self.lista_marcas= []

# añade una nueva marca a la lista.
	def añadir (self, pista):
		self.lista_marcas.append({
		'numero': numero,
		'título': titulo,
		'autor': autor,
		'tiempo_inicio': tiempo_inicio})

# limpia la lista de marcas.
	def limpiar (self):
		self.lista_marcas.clear()


class Marca():
	pass
	#numero, titulo, autor, tiempo_inicio