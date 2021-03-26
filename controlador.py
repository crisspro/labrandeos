import pandas
from marca import *
import pickle

class Controlador():
	def __init__(self):
		self.data  = None
	
	def crearMarca(self, *args, **kwargs):
		marca = Marca(*args, **kwargs)
		self.data.agregarMarca(marca)
		self.save()
		base = open('base.csv', 'w')
		datos = {'Título': [args[0]], 'Autor': [args[1]], 'Tiempo de inicio': [args[2]]}
		datos_pandas = pandas.DataFrame(datos)
		datos_pandas.to_csv('base.csv')
		base.close()
		return marca
	
	def getMarcas(self):
		return self.data.getMarcas()
	
	def load(self):
		""" carga la información del modelo. """
		try:
			f = open("info.cp", "rb")
			self.data = pickle.load(f)
			f.close()
		except FileNotFoundError:
			self.data = Data()
	
	def save(self):
		""" guarda la información del modelo """
		f = open("info.cp", "wb")
		pickle.dump(self.data, f)
		f.close()
		