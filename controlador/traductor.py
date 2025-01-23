import gettext
from locale import getdefaultlocale
import os

import controlador.configuracion


class Traductor():
    def __init__(self):
        self.controlador_opciones = controlador.configuracion.Opciones()
        self.idioma = self.controlador_opciones.consultar_opciones('str', 'general', 'idioma')
        self.ruta = os.path.join('locale')
        self.t = gettext.translation('labrandeos', localedir=self.ruta, languages=[self.idioma])
        self.t.install()
        self._ = self.t.gettext

    def consultar_idioma_defecto(self):
        return getdefaultlocale()[0]
