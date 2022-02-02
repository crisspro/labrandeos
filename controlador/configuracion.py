from configparser import ConfigParser
import os

import modelo.configuracion

class App():
	def __init__(self):
		self.nombre_app = 'CUE Genesis'
		self.autor_app = 'Crisspro'
		self.licencia_app = 'GPL 3.0'
		self.sitio_app = 'https://github.com/crisspro/cuegenesis'
		self.version_app = 'v0.1'


class Opciones():
	def __init__(self):
		self.configparser = ConfigParser()
		self.archivo_configuracion = os.path.join('files', 'user.ini')
		self.configparser.read(self.archivo_configuracion,encoding= 'utf-8')


	def chequear_ini(self):
		if os.path.isfile(self.archivo_configuracion) == False:
			self.guardar_defecto()

	def guardar_opciones(self, seccion, clave, valor):
		archivo = open(self.archivo_configuracion, 'w')
		self.configparser.set(str(seccion), str(clave), str(valor))
		self.configparser.write(self.archivo_configuracion)

	def guardar_defecto(self):
		self.configparser['general']= modelo_configuracion.dic_general
		archivo = open(self.archivo_configuracion, 'w', encoding= 'UTF-8')
		self.configparser.write(archivo)
		archivo.close()

# creación de instancias

modelo_configuracion = modelo.configuracion.Configuracion()
