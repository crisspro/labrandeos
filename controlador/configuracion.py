from configparser import ConfigParser
from locale import getdefaultlocale
import os
import requests
import webbrowser

import modelo.configuracion

class App():
	def __init__(self):
		self.configparser = ConfigParser()
		self.archivo_configuracion = os.path.join('files', 'user.ini')
		self.configparser.read(self.archivo_configuracion,encoding= 'utf-8')
		self.nombre_app = 'CUE Genesis'
		self.autor_app = 'Crisspro'
		self.licencia_app = 'GPL 3.0'
		self.sitio_app = 'https://github.com/crisspro/cuegenesis'
		self.api_app = 'https://api.github.com/repos/crisspro/cuegenesis/releases/latest'
		self.idioma_app = 'en'
		self.version_app = 'v0.1'
		self.actualizado = True


	def verificarNuevaVersion(self):
		try:
			coneccion= requests.get(self.api_app, timeout= 5)
		except:
			print('No hay conección')
		else:
			try:
				v= coneccion.json() ['tag_name']
				if v != self.version_app:
					self.actualizado = False
				else:
					self.actualizado = True
			except KeyError:
				print('No se ha podido establecer la conexión', 'Error.')


	def descargar_version(self):
		coneccion= requests.get(self.api_app, timeout= 5)
		dw= coneccion.json() ['assets']
		for i in dw:
			dw= i['browser_download_url']
		webbrowser.open(dw)



class Opciones():
	def __init__(self):
		self.configparser = ConfigParser()
		self.archivo_configuracion = os.path.join('files', 'user.ini')
		self.configparser.read(self.archivo_configuracion,encoding= 'utf-8')


	def chequear_ini(self):
		if os.path.isfile(self.archivo_configuracion) == False:
			self.guardar_defecto()

	def guardar_defecto(self):
		self.configparser['general']= modelo_configuracion.dic_general
		archivo = open(self.archivo_configuracion, 'w', encoding= 'UTF-8')
		self.configparser.write(archivo)
		archivo.close()

	def consultar_opciones(self,seccion, clave):
		self.configparser.read(self.archivo_configuracion,encoding= 'utf-8')
		return self.configparser.getboolean(seccion, clave)


	def refrescar_ini(self):
		self.configparser = ConfigParser()
		self.archivo_configuracion = os.path.join('files', 'user.ini')
		self.configparser.read(self.archivo_configuracion,encoding= 'utf-8')

# creación de instancias

modelo_configuracion = modelo.configuracion.Configuracion()
