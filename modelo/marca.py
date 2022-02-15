class Data():
	def __init__(self, *ARGS, **KWARGS):
		self.id = 0
		self.titulo= 'Sin título'
		self.autor= 'Sin autor'
		self.tiempo_inicio = 0
		self.milesimas = 0


		# lista de  marcas.
		self.lista_marcas= []

	# añade una nueva marca a la lista.
	def agregarMarca(self, marca):
		self.lista_marcas.append(marca)

	#ordena las marcas
	def ordenar(self):
		self.lista_marcas.sort(key= lambda marca:marca.milesimas)
		id = 0
		for marca in self.lista_marcas:
			marca.id = id+1
			id = id+1

	def borrar_marca(self, id):
		self.lista_marcas.pop(id)

	# limpia la lista de marcas.
	def limpiar (self):
		self.lista_marcas.clear()
	
	def getMarcas(self):
		return self.lista_marcas


class Marca():
	def __init__(self, id, titulo, autor, tiempo_inicio, milesimas):
		self.id = id
		self.titulo = titulo
		self.autor = autor
		self.tiempo_inicio = tiempo_inicio
		self.milesimas = milesimas

	def filtrar_tiempo_inicio_cue(self):
		tiempo = self.tiempo_inicio.split()
		minutos = int(tiempo[0]) * 60 + int(tiempo[2]) 
		tiempo = str(minutos).zfill(2) +':'+ tiempo[4].zfill(2) +':'+ tiempo[6].zfill(2)
		return tiempo



