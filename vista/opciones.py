import configparser

import wx

import controlador.configuracion


class Opciones(wx.Dialog):
	def __init__(self, parent, title):
		super().__init__(parent, title= title)
		self.Center()
		self.archivo_configuracion = controlador_opciones.archivo_configuracion
		configparser.read(self.archivo_configuracion,encoding= 'utf-8')


		# Creación de controles
		panel1 = wx.Panel(self)
		self.l_idioma = wx.StaticText(panel1, -1, 'Idioma')
		self.lista_idioma = ['Español', 'Inglés']
		self.com_idioma = wx.ComboBox(panel1, -1, configparser.get('general', 'idioma'), choices= self.lista_idioma )
		self.com_idioma.SetFocus()
		self.cas_cue_id = wx.CheckBox(panel1, -1, 'Añadir índice al exportar marcas')
		self.cas_cue_id.SetValue(configparser.getboolean('general', 'cue_id'))
		self.cas_sonido_actualizacion = wx.CheckBox(panel1, -1, 'Sonido al detectar nueva actualización')
		self.cas_sonido_actualizacion.SetValue(configparser.getboolean('general', 'sonido_actualizacion'))
		self.cast_sonido_marca = wx.CheckBox(panel1, -1, 'Sonido al crear una nueva marca')
		self.cast_sonido_marca.SetValue(configparser.getboolean('general', 'sonido_marca'))
		self.cas_sonido_generar = wx.CheckBox(panel1, -1, 'Sonido al generar el archivo CUE')
		self.cas_sonido_generar.SetValue(configparser.getboolean('general', 'sonido_generar'))
		self.bt_aceptar = wx.Button(panel1, wx.ID_OK, '&Aceptar')
		self.bt_aceptar.SetDefault()
		self.bt_cancelar = wx.Button(panel1, wx.ID_CANCEL, '&Cancelar')

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
		configparser.set('general', 'idioma', self.com_idioma.GetValue())
		configparser.set('general', 'cue_id', str(self.cas_cue_id.GetValue()))
		configparser.set('general', 'sonido_actualizacion', str(self.cas_sonido_actualizacion.GetValue()))
		configparser.set('general', 'sonido_marca', str(self.cast_sonido_marca.GetValue()))
		configparser.set('general', 'sonido_generar', str(self.cas_sonido_generar.GetValue()))
		archivo = open(self.archivo_configuracion, 'w', encoding= 'UTF-8')
		configparser.write(archivo)



# Creación de instancias

configparser = configparser.ConfigParser()
controlador_opciones = controlador.configuracion.Opciones()