#título: CUE Genesis
#Copyriht (C) 2022 Crisspro <crisspro@hotmail.com>
#lisencia: GPL-3.0

import wx

from controlador.controlador import Controlador
from controlador.configuracion import Opciones 
from vista.grafica import Programa






App= wx.App()
controlador = Controlador()
controlador_opciones = Opciones()

controlador.verificarNuevaVersion()
controlador_opciones.chequear_ini()
controlador.load()
controlador.limpiar_temporal()
Programa(None, title= 'CUE Genesis', controlador = controlador)
App.MainLoop()