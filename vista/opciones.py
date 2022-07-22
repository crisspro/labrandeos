import wx

import controlador.configuracion
import controlador.traductor


class Opciones(wx.Dialog):
	def __init__(self, parent, title):
		super().__init__(parent, title= title)
		self.Center()
		self.controlador_app = controlador.configuracion.App()
		self.controlador_opciones = controlador.configuracion.Opciones()
		controlador.traductor.Traductor('opciones')

		# Creación de controles
		panel1 = wx.Panel(self)
		self.l_idioma = wx.StaticText(panel1, -1, _('Idioma'))
		self.lista_idioma = [ _('Español'), _('Inglés')]
		self.com_idioma = wx.ComboBox(panel1, -1, self.completar_idioma(), choices= self.lista_idioma, style= wx.CB_READONLY)
		self.com_idioma.SetFocus()
		self.cas_cue_id = wx.CheckBox(panel1, -1, _('Añadir índice al exportar marcas'))
		self.cas_cue_id.SetValue(self.controlador_opciones.consultar_opciones('bool', 'general', 'cue_id'))
		self.cas_sonido_actualizacion = wx.CheckBox(panel1, -1, _('Sonido al detectar nueva actualización'))
		self.cas_sonido_actualizacion.SetValue(self.controlador_opciones.consultar_opciones('bool', 'general', 'sonido_actualizacion'))
		self.cast_sonido_marca = wx.CheckBox(panel1, -1, _('Sonido al crear una nueva marca'))
		self.cast_sonido_marca.SetValue(self.controlador_opciones.consultar_opciones('bool', 'general', 'sonido_marca'))
		self.cas_sonido_generar = wx.CheckBox(panel1, -1, _('Sonido al generar el archivo CUE'))
		self.cas_sonido_generar.SetValue(self.controlador_opciones.consultar_opciones('bool', 'general', 'sonido_generar'))
		self.bt_aceptar = wx.Button(panel1, wx.ID_OK, _('&Aceptar'))
		self.bt_aceptar.SetDefault()
		self.bt_cancelar = wx.Button(panel1, wx.ID_CANCEL, _('&Cancelar'))

# Creación de sizers

		sz1 = wx.BoxSizer(wx.VERTICAL)
		sz1.Add(self.l_idioma)
		sz1.Add(self.com_idioma)
		sz1.Add(self.cas_sonido_actualizacion)
		sz1.Add(self.cast_sonido_marca)
		sz1.Add(self.cas_sonido_generar)

		sz2 = wx.BoxSizer(wx.HORIZONTAL)
		sz1.Add(sz2)
		sz2.Add(self.bt_aceptar)
		sz2.Add(self.bt_cancelar)

		panel1.SetSizer(sz1)

	def guardar_opciones(self):
		self.controlador_opciones.guardar_opciones('general', 'idioma', self.resumir_idioma())
		self.controlador_opciones.guardar_opciones('general', 'cue_id', str(self.cas_cue_id.GetValue()))
		self.controlador_opciones.guardar_opciones('general', 'sonido_actualizacion', str(self.cas_sonido_actualizacion.GetValue()))
		self.controlador_opciones.guardar_opciones('general', 'sonido_marca', str(self.cast_sonido_marca.GetValue()))
		self.controlador_opciones.guardar_opciones('general', 'sonido_generar', str(self.cas_sonido_generar.GetValue()))


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



