#título: CUE Genesis
#autor: Crisspro
#lisencia: GPL-3.0

import wx


class Configuracion(wx.Dialog):
	def __(self, parent, title):
		super().__init__(parent, title = title)
		self.Center()