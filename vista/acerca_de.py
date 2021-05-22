import webbrowser
import wx

from controlador import Controlador
from .grafica import *

class Acerca_de(wx.Dialog):
	def __init__(self, parent, title):
		super().__init__(parent, title= title)
		self.Center()
		
		panel = wx.Panel(self)
		self.in_info = wx.TextCtrl(panel, -1, nombre_app + ' ' + version_app + '\n' + 'Autor: ' + autor_app + '\n' + 'Licencia: ' + lisencia_app, style= wx.TE_MULTILINE)
		self.bt_visitar = wx.Button(panel, -1, '&Visitar sitio del proyecto')
		self.Bind(wx.EVT_BUTTON, self.visitar_sitio, self.bt_visitar)
		self.bt_cerrar = wx.Button(panel, wx.ID_OK, '&Cerrar')

		sz1 = wx.BoxSizer(wx.VERTICAL)

		sz1.Add(self.in_info)
		sz1.Add(self.bt_visitar)
		sz1.Add(self.bt_cerrar)

		panel.SetSizer(sz1)

	def visitar_sitio(self, event):
		webbrowser.open('https//github.com/crisspro/cuegenesis')