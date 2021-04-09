import pickle

from modelo.marca import *
from modelo.tiempo import Tiempo

class Controlador():
	def __init__(self):
		self.data  = None
		self.ruta_proyecto = 'temp.proyecto.cgp'
	
	def crearMarca(self, *args, **kwargs):
		marca = Marca(*args, **kwargs)
		self.data.agregarMarca(marca)
		self.save()
		return marca

	def getMarcas(self):
		return self.data.getMarcas()
	
	def load(self):
		""" carga la información del modelo. """
		try:
			f = open(self.ruta_proyecto , "rb")
			self.data = pickle.load(f)
			f.close()
		except FileNotFoundError:
			self.data = Data()
	
	def save(self):
		""" guarda la información del modelo """
		f = open(self.ruta_proyecto , 'wb')
		pickle.dump(self.data, f)
		f.close()


