import webbrowser
import wx

from controlador import Controlador
from .grafica import *

class Acerca_de(wx.Dialog):
	def __init__(self, parent, title):
		super().__init__(parent, title= title)
		self.Center()
		
		panel = wx.Panel(self)
		self.in_info = wx.TextCtrl(panel, -1, 'Versión: ' + version_app + '\n' + 'autor: ' + autor_app + '\n' + 'Licencia: ' + lisencia_app, style= wx.TE_MULTILINE)
		self.bt_visitar = wx.Button(panel, -1, '&Visitar el sitio del proyecto')
		self.Bind(wx.EVT_BUTTON, self.visitar_sitio, self.bt_visitar)
		bt_cerrar = wx.Button(panel, wx.ID_OK, '&Cerrar')

	def visitar_sitio(self, event):
		webbrowser.open('https//github.com/crisspro/cuegenesis')