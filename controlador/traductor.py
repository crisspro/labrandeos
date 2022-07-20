import gettext
from locale import getdefaultlocale
import os


class Traductor():
	def __init__(self, idioma, modulo):
		self.idioma = idioma
		self.modulo = modulo
		self.ruta = os.path.join('vista', 'locale')
		self.traducir()


	def traducir(self):
		t = gettext.translation(self.modulo, localedir= self.ruta, languages=[self.idioma])
		t.install()

	def consultar_idioma_defecto(self):
		returngetdefaultlocale()[0]
