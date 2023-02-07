import gettext
from locale import getdefaultlocale
import os

import controlador.configuracion

class Traductor():
	def __init__(self, modulo):
		self.controlador_opciones = controlador.configuracion.Opciones()
		self.idioma = self.controlador_opciones.consultar_opciones('str', 'general', 'idioma')
		self.modulo = modulo
		self.ruta = os.path.join('vista', 'locale')
		self.traducir()


	def traducir(self):
		t = gettext.translation(self.modulo, localedir= self.ruta, languages=[self.idioma])
		t.install()

	def consultar_idioma_defecto(self):
		return getdefaultlocale()[0]
