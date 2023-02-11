#título: CUE Genesis
#Copyriht (C) 2023 Crisspro <crisspro@hotmail.com>
#lisencia: GPL-3.0

import sys

import wx

from controlador.controlador import Controlador
import controlador.configuracion
from vista.grafica import Programa


def alertar_instancia():
	if controlador_app.verificar_instancia():
		wx.MessageBox(controlador_app.nombre_app + ' ya se está ejecutando.', 'Aviso')
		sys.exit(1)


App= wx.App()
controlador_app = controlador.configuracion.App()
alertar_instancia()
controlador_controlador = Controlador()
controlador_opciones = controlador.configuracion.Opciones()
controlador_opciones.chequear_ini()
controlador_controlador.limpiar_temporal()
controlador_controlador.save()
Programa(None, title= controlador_app.nombre_app, controlador = controlador_controlador, app= controlador_app, opciones= controlador_opciones)

App.MainLoop()

