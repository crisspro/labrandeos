#título: Labrandeos
#Copyriht (C) 2023 Crisspro <crisspro@hotmail.com>
#lisencia: GPL-3.0

import sys

import wx

from controlador.controlador import Controlador
import controlador.configuracion
from controlador.traductor import Traductor
from vista.principal import Frame


App= wx.App()
traductor = Traductor('Labrandeos')
controlador_app = controlador.configuracion.App()
controlador_controlador = Controlador()
controlador_opciones = controlador.configuracion.Opciones()
controlador_opciones.chequear_ini()
controlador_controlador.limpiar_temporal()
controlador_controlador.save()
Frame(None, title= controlador_app.nombre_app, controlador = controlador_controlador, app= controlador_app, opciones= controlador_opciones)

App.MainLoop()

