class Reproductor():
	def __init__(self):
		self.estado = 'stop'
		self.pista = None
		self.tiempo_actual = 0
		self.volumen = 1
		self.marca_id = 0


	def cargar(self, pista):
		self.pista = pista

	def reproducir(self):
		self.estado = 'play'

	def pausar(self):
		self.estado = 'pause'

	def detener(self):
		self.estado = 'stop'