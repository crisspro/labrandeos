class Historial():
	def __init__(self):
		self.pila1 = []
		self.pila2 = []

	def apilar(self, objeto):
		self.pila1.append(objeto)
		self.pila2.clear()

	def desapilar(self):
		if len(self.pila1) != 0:
			self.pila2.append(self.pila1[-1])
			return self.pila1.pop()

	def es_vacia(self):
		return self.pila1 == [],  self.pila2 == []