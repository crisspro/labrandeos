class Historial():
	def __init__(self):
		self.pila1 = []
		self.pila2 = []

	def apilar(self, objeto):
		self.pila1.append(objeto)


	def desapilar(self):
		if len(self.pila1) != 0:
			return self.pila1.pop()

	def reapilar(self):
		if len(self.pila2) != 0:
			self.pila1.append(self.pila2[-1])
			self.pila2.pop()
			return self.pila2[-1]

	def limpiar(self):
		self.pila1.clear()
		self.pila2.clear()

	def es_vacia(self):
		return self.pila1 == [],  self.pila2 == []