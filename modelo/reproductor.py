class Reproductor():
	def __init__(self):
		self.estado = 'stop'
		self.pista = None
		self.tiempo_actual = 0
		self.volumen = 100


	def cargar(self, pista):
		self.pista = pista

	def refrescar(self):
		self.__init__()

	def reproducir(self):
		self.estado = 'play'

	def pausar(self):
		self.estado = 'pause'

	def detener(self):
		self.estado = 'stop'