class Pila():
	def __init__(self):
		self.historial = []

	def apilar(self, objeto):
		self.historial.append(objeto)

	def desapilar(self):
		if len(self.historial) != 0:
			return self.historial.pop()

	def es_vacia(self):
		return self.historial == []