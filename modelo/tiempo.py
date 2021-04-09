class Tiempo():
	def __init__(self, parent, title):
		self.horas = horas
		self.minutos = minutos
		self.segundos = segundos
		self.marcos = marcos

	def __str__(self):
		return '{} horas:{} minutos:{} segundos:{} marcos'.format(self.horas, self.minutos, self.segundos, self.marcos)

	def __add__(self, t):
		pass

	# convierte milésimas en horas,minutos,segundos y marcos.
	def convertir (self, milesimas):
		total_marcos= int(milesimas*75/1000) #convierte milésimas a cantidad de marcos
		self.marcos= total_marcos%75 
		self.segundos= int(total_marcos/75%60)
		self.minutos= int(total_marcos/60/75%60)
		self.total_minutos= int(total_marcos/60/75)
		self.horas= int(total_marcos/60/60/75)
