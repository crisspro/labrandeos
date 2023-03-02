import wx

import controlador.configuracion


class Opciones(wx.Dialog):
	def __init__(self, parent, title, opciones):
		super().__init__(parent, title= title)
		self.Center()
		self.controlador_app = controlador.configuracion.App()
		self.controlador_opciones = opciones

		# Creación de controles
		panel1 = wx.Panel(self)
		self.l_idioma = wx.StaticText(panel1, -1, _('Idioma'))
		self.lista_idioma = [ _('Español'), _('Inglés')]
		self.com_idioma = wx.ComboBox(panel1, -1, self.completar_idioma(), choices= self.lista_idioma, style= wx.CB_READONLY)
		self.com_idioma.SetFocus()
		self.cas_indice = wx.CheckBox(panel1, -1, _('Añadir índice al exportar marcas'))
		self.cas_indice.SetValue(self.controlador_opciones.consultar_opciones('bool', 'general', 'indice'))
		self.cas_abrir_carpeta = wx.CheckBox(panel1, -1, _('Abrir carpeta de destino al exportar'))
		self.cas_abrir_carpeta.SetValue(self.controlador_opciones.consultar_opciones('bool', 'general', 'abrir_carpeta'))
		self.cas_detectar_actualizacion = wx.CheckBox(panel1, -1, _('Detectar si hay actualizaciones al iniciar'))
		self.cas_detectar_actualizacion.SetValue(self.controlador_opciones.consultar_opciones('bool', 'general', 'detectar_actualizacion'))
		self.cas_sonido_actualizacion = wx.CheckBox(panel1, -1, _('Sonido al detectar nueva actualización'))
		self.cas_sonido_actualizacion.SetValue(self.controlador_opciones.consultar_opciones('bool', 'general', 'sonido_actualizacion'))
		self.cast_sonido_marca = wx.CheckBox(panel1, -1, _('Sonido al crear una nueva marca'))
		self.cast_sonido_marca.SetValue(self.controlador_opciones.consultar_opciones('bool', 'general', 'sonido_marca'))
		self.cas_sonido_exportar = wx.CheckBox(panel1, -1, _('Sonido al exportar el archivo CUE'))
		self.cas_sonido_exportar.SetValue(self.controlador_opciones.consultar_opciones('bool', 'general', 'sonido_exportar'))
		self.bt_aceptar = wx.Button(panel1, wx.ID_OK, _('&Aceptar'))
		self.bt_aceptar.SetDefault()
		self.bt_cancelar = wx.Button(panel1, wx.ID_CANCEL, _('&Cancelar'))

# Creación de sizers

		sz1 = wx.BoxSizer(wx.VERTICAL)
		sz1.Add(self.l_idioma)
		sz1.Add(self.com_idioma)
		sz1.Add(self.cas_indice)
		sz1.Add(self.cas_abrir_carpeta)
		sz1.Add(self.cas_sonido_actualizacion)
		sz1.Add(self.cast_sonido_marca)
		sz1.Add(self.cas_sonido_exportar)

		sz2 = wx.BoxSizer(wx.HORIZONTAL)
		sz1.Add(sz2)
		sz2.Add(self.bt_aceptar)
		sz2.Add(self.bt_cancelar)

		panel1.SetSizer(sz1)

	def guardar_opciones(self):
		self.controlador_opciones.modelo_configuracion.idioma_app = self.resumir_idioma()
		self.controlador_opciones.guardar_opciones('general', 'indice', str(self.cas_indice.GetValue()))
		self.controlador_opciones.guardar_opciones('general', 'abrir_carpeta', str(self.cas_abrir_carpeta.GetValue()))
		self.controlador_opciones.guardar_opciones('general', 'detectar_actualizacion', str(self.cas_detectar_actualizacion.GetValue()))
		self.controlador_opciones.guardar_opciones('general', 'sonido_actualizacion', str(self.cas_sonido_actualizacion.GetValue()))
		self.controlador_opciones.guardar_opciones('general', 'sonido_marca', str(self.cast_sonido_marca.GetValue()))
		self.controlador_opciones.guardar_opciones('general', 'sonido_exportar', str(self.cas_sonido_exportar.GetValue()))


	def completar_idioma(self):
		prefijo = self.controlador_opciones.consultar_opciones('str', 'general', 'idioma') 
		if prefijo == 'es':
			return _('Español')
		elif prefijo == 'en':
			return _('Inglés')

	def resumir_idioma(self):
		idioma = self.com_idioma.GetValue()
		if idioma == _('Español'):
			return 'es'
		elif idioma == _('Inglés'):
			return 'en'



