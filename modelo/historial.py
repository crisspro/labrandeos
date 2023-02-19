class Historial():
	def __init__(self):
		self.pila1 = []
		self.pila2 = []

	def apilar(self, objeto, limpiar= True):
		self.pila1.append(objeto)
		if limpiar: 
			self.pila2.clear()

	def desapilar(self):
		if len(self.pila1) > 0:
			return self.pila1.pop()

	def reservar(self, objeto):
		self.pila2.append(objeto)

	def reapilar(self):
		if len(self.pila2) > 0:
			return self.pila2.pop()


	def limpiar(self):
		self.pila1.clear()
		self.pila2.clear()

	def es_vacia(self):
		return self.pila1 == [],  self.pila2 == []