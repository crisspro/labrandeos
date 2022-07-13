#título: CUE Genesis
#Copyriht (C) 2022 Crisspro <crisspro@hotmail.com>
#lisencia: GPL-3.0

import wx

from controlador.controlador import Controlador
import controlador.configuracion
from vista.grafica import Programa


App= wx.App()
controlador_controlador = Controlador()
controlador_opciones = controlador.configuracion.Opciones()
controlador_app = controlador.configuracion.App()
controlador_opciones.chequear_ini()
controlador_controlador.load()
controlador_controlador.limpiar_temporal()
Programa(None, title= 'CUE Genesis', controlador = controlador_controlador, app= controlador_app, opciones= controlador_opciones)

App.MainLoop()