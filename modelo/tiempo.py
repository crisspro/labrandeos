class Tiempo():
	def __init__(self, *ARGS, **KWARGS):
		self.horas = 0
		self.minutos = 0
		self.segundos = 0
		self.marcos = 0
		self.milesimas = 0

	# convierte milésimas en horas,minutos,segundos y marcos.
	def convertir(self, milesimas):
		total_marcos= int(milesimas*75/1000) #convierte milésimas a cantidad de marcos
		self.marcos= total_marcos%75 
		self.segundos= int(total_marcos/75%60)
		self.minutos= int(total_marcos/60/75%60)
		self.total_minutos= int(total_marcos/60/75)
		self.horas= int(total_marcos/60/60/75)

	def reconvertir(self):
		marcos = int(self.marcos) * 1000/75
		segundos = int(self.segundos) * 1000
		minutos = self.minutos *60 * 1000
		horas = int(self.horas) * 60 *60 * 1000
		self.milesimas = int(horas+minutos+segundos+marcos)
		return self.milesimas