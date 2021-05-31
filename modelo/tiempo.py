
class Tiempo():
	def __init__(self):
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


