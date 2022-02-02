import configparser

import wx

class Opciones(wx.Dialog):
	def __init__(self, parent, title):
		super().__init__(parent, title= title)
		self.Show()
		self.Center()

# Creación de controles
		panel1 = wx.Panel(self)
		self.l_idioma = wx.StaticText(panel1, -1, 'Idioma')
		self.lista_idioma = ['english', 'spanish']
		self.com_idioma = wx.ComboBox(panel1, -1, 'Spanish', choices= self.lista_idioma )
		self.com_idioma.SetFocus()
		self.cas_sonido_actualizacion = wx.CheckBox(panel1, -1, 'Activar sonido al detectar nueva actualización')
		self.cast_sonido_marca = wx.CheckBox(panel1, -1, 'Activar sonido al crear una nueva marca')
		self.cas_sonido_generar = wx.CheckBox(panel1, -1, 'Activar sonido al generar el archivo CUE')
		self.bt_aceptar = wx.Button(panel1, -1, '&Aceptar', style= wx.ID_OK)
		self.bt_cancelar = wx.Button(panel1, -1, '&Cancelar', style= wx.ID_CANCEL)

# Creación de sizers

		sz1 = wx.BoxSizer(wx.VERTICAL)
		sz1.Add(self.l_idioma)
		sz1.Add(self.com_idioma)
		sz1.Add(self.cas_sonido_actualizacion)
		sz1.Add(self.cast_sonido_marca)
		sz1.Add(self.cas_sonido_generar)

		panel1.SetSizer(sz1)
		sz2 = wx.BoxSizer(wx.HORIZONTAL)
		sz1.Add(sz2)
		sz2.Add(self.bt_aceptar)
		sz2.Add(self.bt_cancelar)


# Creación de instancias

configparser = configparser.ConfigParser()