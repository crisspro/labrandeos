import wx

import controlador.configuracion

class Opciones(wx.Dialog):
	def __init__(self, parent, title, opciones):
		super().__init__(parent, title= title)
		self.Center()
		self.controlador_app = controlador.configuracion.App()
		self.controlador_opciones = opciones
		self.Show()

		self.libreta = wx.Notebook(self)
		self.pagina1 = General(self.libreta, self.controlador_opciones)
		self.pagina2 = Audio(self.libreta)
		self.libreta.AddPage(self.pagina1, _('General'))
		self.libreta.AddPage(self.pagina2, _('Audio'))
		self.botones_dialog = wx.StdDialogButtonSizer()
		self.bt_aceptar = wx.Button(self, wx.ID_OK, _('&Aceptar'))
		self.bt_aceptar.SetDefault()
		self.bt_cancelar = wx.Button(self, wx.ID_CANCEL, _('&Cancelar'))
		self.botones_dialog.AddButton(self.bt_aceptar)
		self.botones_dialog.AddButton(self.bt_cancelar)
		self.botones_dialog.Realize()


		# creación de sizers
		self.sz1 = wx.BoxSizer(wx.VERTICAL)
		self.sz1.Add(self.libreta, 1, wx.EXPAND | wx.ALL, 5)
		self.sz1.Add(self.botones_dialog, 0, wx.ALIGN_RIGHT | wx.ALL, 5)
		
		self.SetSizerAndFit(self.sz1)





class General(wx.Panel):
	def __init__(self, parent, controlador_opciones):
		wx.Panel.__init__(self,parent)
		self.controlador_opciones = controlador_opciones


		# Creación de controles
#		self = wx.Panel(self)
		self.l_idioma = wx.StaticText(self, -1, _('Idioma'))
		self.lista_idioma = [ _('Español'), _('Inglés')]
		self.com_idioma = wx.ComboBox(self, -1, self.completar_idioma(), choices= self.lista_idioma, style= wx.CB_READONLY)
		self.com_idioma.SetFocus()
		self.cas_indice = wx.CheckBox(self, -1, _('Añadir índice al exportar marcas'))
		self.cas_indice.SetValue(self.controlador_opciones.consultar_opciones('bool', 'general', 'indice'))
		self.cas_abrir_carpeta = wx.CheckBox(self, -1, _('Abrir carpeta de destino al exportar'))
		self.cas_abrir_carpeta.SetValue(self.controlador_opciones.consultar_opciones('bool', 'general', 'abrir_carpeta'))
		self.cas_detectar_actualizacion = wx.CheckBox(self, -1, _('Detectar si hay actualizaciones al iniciar'))
		self.cas_detectar_actualizacion.SetValue(self.controlador_opciones.consultar_opciones('bool', 'general', 'detectar_actualizacion'))
		self.cas_sonido_actualizacion = wx.CheckBox(self, -1, _('Sonido al detectar nueva actualización'))
		self.cas_sonido_actualizacion.SetValue(self.controlador_opciones.consultar_opciones('bool', 'general', 'sonido_actualizacion'))
		self.cast_sonido_marca = wx.CheckBox(self, -1, _('Sonido al crear una nueva marca'))
		self.cast_sonido_marca.SetValue(self.controlador_opciones.consultar_opciones('bool', 'general', 'sonido_marca'))
		self.cas_sonido_exportar = wx.CheckBox(self, -1, _('Sonido al exportar el archivo CUE'))
		self.cas_sonido_exportar.SetValue(self.controlador_opciones.consultar_opciones('bool', 'general', 'sonido_exportar'))


# Creación de sizers

		sz1 = wx.BoxSizer(wx.VERTICAL)
		sz1.Add(self.l_idioma)
		sz1.Add(self.com_idioma)
		sz1.Add(self.cas_indice)
		sz1.Add(self.cas_abrir_carpeta)
		sz1.Add(self.cas_sonido_actualizacion)
		sz1.Add(self.cast_sonido_marca)
		sz1.Add(self.cas_sonido_exportar)

		self.SetSizer(sz1)


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


class Audio(wx.Panel):
	def __init__(self, parent):
		wx.Panel.__init__(self, parent)

#		self = wx.Panel(self)
		self.l_formato = wx.StaticText(self, -1, _('Formato:'))
		self.lista_formato = ['Automático', 'aac', 'flac', 'mp3', 'ogg', 'wav', 'wma']
		self.com_formato = wx.ComboBox(self, -1, _('Automático'), choices= self.lista_formato, style= wx.CB_READONLY)
		self.Bind(wx.EVT_COMBOBOX, self.habilitar_formato, self.com_formato)
		self.l_taza_bit = wx.StaticText(self, -1, _('Taza de bit:'))
		self.lista_taza_bit = [_('Automático'), '92 kb/s', '128 kb/s', '192 kb/s', '256 kb/s', '320 kb/s']
		self.com_taza_bit = wx.ComboBox(self, -1, _('Automático'), choices= self.lista_taza_bit, style= wx.CB_READONLY)
		self.l_modo_taza_bit = wx.StaticText(self, -1, _('Modo de taza de bit:'))
		self.lista_modo_taza_bit = [_('Automático'), _('Variable (vbr)'), _('Constante (cbr)')]
		self.com_modo_taza_bit = wx.ComboBox(self, -1, _('Automático'), choices= self.lista_modo_taza_bit, style= wx.CB_READONLY)
		self.l_velocidad_muestreo = wx.StaticText(self, -1, _('Velocidad de muestreo:'))
		self.lista_velocidad_muestreo = [_('Automático'), '6000 Hz', '8000 Hz', '16000 Hz', '22050 Hz', '24000 Hz', '32000 Hz', '44100 Hz', '48000 Hz', '88200 Hz', '96000 Hz', '176400 Hz', '192000 Hz']
		self.com_velocidad_muestreo = wx.ComboBox(self, -1, _('Automático'), choices= self.lista_velocidad_muestreo, style= wx.CB_READONLY)
		self.cas_normalizar = wx.CheckBox(self, -1, 'Normalizar')
		self.cas_silencio = wx.CheckBox(self, -1, 'Añadir silencio al final de cada pista')

		self.sz1 = wx.BoxSizer(wx.VERTICAL)
		
		self.sz1.Add(self.l_formato)
		self.sz1.Add(self.com_formato)
		self.sz1.Add(self.l_taza_bit)
		self.sz1.Add(self.com_taza_bit)
		self.sz1.Add(self.l_modo_taza_bit)
		self.sz1.Add(self.com_modo_taza_bit)
		self.sz1.Add(self.l_velocidad_muestreo)
		self.sz1.Add(self.com_velocidad_muestreo)
		self.sz1.Add(self.cas_normalizar)
		self.sz1.Add(self.cas_silencio)
		
		self.SetSizer(self.sz1)


	def habilitar_formato(self, event):
		''' habilita controles según formato escogido '''
		if self.com_formato.GetValue() == _('Automático'):
			self.com_modo_taza_bit.Enable(False)
			self.com_taza_bit.Enable(False)
			self.com_velocidad_muestreo.Enable(False)
		elif self.com_formato.GetValue() == 'aac':
			self.com_modo_taza_bit.Enable(False)
			self.l_taza_bit.SetLabel(_('Calidad:'))
			self.lista_taza_bit = ['0 (máxima calidad)', '1', '2', '3', '4', '5', '6', '7', '8', '9 (menor calidad)']
			self.com_taza_bit.Enable(True)
