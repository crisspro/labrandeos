import pandas
from marca import *

class Controlador():
	def __init__(self):
		self.data  = Data()
	
	def crearMarca(self, *args, **kwargs):
		marca = Marca(*args, **kwargs)
		self.data.agregarMarca(marca)
		base = open('base.csv', 'w')
		datos = {'Título': [args[0]], 'Autor': [args[1]], 'Tiempo de inicio': [args[2]]}
		datos_pandas = pandas.DataFrame(datos)
		datos_pandas.to_csv('base.csv')
		base.close()
		return marca