# título: Labrandeos
# Copyriht (C) 2025 Crisspro <crisspro@hotmail.com>
# lisencia: GPL-3.0

import os

import wx

from controlador.traductor import Traductor
from controlador.controlador import Controlador
import controlador.configuracion
from vista.principal import Frame


def crear_carpeta():
    ''' crea la carpeta Labrandeos en appdata del usuario'''
    if os.path.exists(os.path.join(os.environ['LOCALAPPDATA'], 'Labrandeos')) == False:
        os.makedirs(os.path.join(os.environ['LOCALAPPDATA'], 'Labrandeos'))


App = wx.App()
controlador_app = controlador.configuracion.App()
controlador_controlador = Controlador()
controlador_opciones = controlador.configuracion.Opciones()
crear_carpeta()
controlador_opciones.chequear_ini()
controlador_opciones.guardar_idioma()
traductor = Traductor('labrandeos')
controlador_controlador.limpiar_temporal()
controlador_controlador.save()
Frame(None, title=controlador_app.nombre_app, controlador=controlador_controlador, app=controlador_app, opciones=controlador_opciones)

App.MainLoop()
