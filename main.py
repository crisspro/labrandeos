#título: CUE Genesis
#autor: Crisspro
#lisencia: GPL-3.0.

import wx
from controlador import Controlador 
from grafica import Programa

App= wx.App()
controlador = Controlador()
controlador.load()
Programa(None, title= 'CUE Genesis', controlador=controlador)
App.MainLoop()