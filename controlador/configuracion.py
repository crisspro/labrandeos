from configparser import ConfigParser
import os
import webbrowser

import modelo.configuracion

class App():
	def __init__(self):
		self.nombre_app = 'CUE Genesis'
		self.autor_app = 'Crisspro'
		self.licencia_app = 'GPL 3.0'
		self.sitio_app = 'https://github.com/crisspro/cuegenesis'
		self.api_app = 'https://api.github.com/repos/crisspro/keyzoneclassic-ahk/releases/latest'
		self.version_app = 'v0.1'



	def verificarNuevaVersion(self):
		try:
			link= self.api_app
			coneccion= requests.get(link, timeout= 5)
		except(requests.ConectionError, requests.Timeout):
			print('No hay conección')
		else:
			try:
				v= coneccion.json() ['tag_name']
			except KeyError:
				print('No se ha podido establecer la conexión', 'Error.')
			if v != self.version_app:
				self.actualizado = False
				wx.adv.Sound.PlaySound(os.path.join('vista', 'sounds', 'nueva_version.wav'))
				resp= wx.MessageBox('Hay disponible una nueva versión de ' + self.nombre_app + '(' + v + ')' + '. ¿Quieres descargarla ahora?', caption= 'Aviso', style= wx.YES_NO)
				if resp == wx.YES:
					dw= coneccion.json() ['assets']
					for i in dw:
						dw= i['browser_download_url']
					webbrowser.open(dw)
					self.Close()
			else:
				self.actualizado = True


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

# creación de instancias

modelo_configuracion = modelo.configuracion.Configuracion()
