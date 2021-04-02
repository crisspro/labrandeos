class Tiempo():
	def __init__(self, hora=0, minutos=0, segundos=0, marcos=0):
		self.hours  = hora
		self.mins = minutos
		self.sec = segundos
		self.mark = marcos
	
	def __str__(self):
		return "tiempo: {} horas, {} minutos, {} segundos, {} marcos.".format(self.hours, self.mins, self.sec, self.mark)
	
	def __add__(self, t):
		return Tiempo(hora=self.hours+t.hours,
			minutos=self.mins+t.mins,
			segundos=self.sec+t.sec,
			marcos=self.mark+t.mark)
	
	def agregarMilesima(self, ms):
		self.sec += ms//1000
	
	def getMins(self):
		if self.mins > 10:
			return str(self.mins)
		else:
			return "0"+str(self.mins)