#título: CUE Genesis
#autor: Crisspro
#lisencia: GPL-3.0.


import pdb
import webbrowser
import wx

from controlador import Controlador 
from vista.grafica import Programa



#verificarNuevaVersion()


App= wx.App()
controlador = Controlador()
controlador.load()
Programa(None, title= 'CUE Genesis', controlador=controlador)
App.MainLoop()