import wx
from controlador.traductor import Traductor


class Informacion_medios(wx.Dialog):
	def __init__(self, parent, title, controlador):
		super().__init__(parent, title= title)
		self.Center()
		Traductor('informacion_medios')
		self.controlador = controlador

		self.panel = wx.Panel(self)
		self.lista_datos = ['nombre: ' + self.controlador.pista.nombre + self.controlador.pista.extencion,
		'Duración: ',
		'Formato: ' + str(self.controlador.comprobar_medios(self.controlador.pista.ruta)[1].format),
		'Tasa de bits: ' + str(self.controlador.comprobar_medios(self.controlador.pista.ruta)[1].other_bit_rate),
		'Velocidad de muestreo: ' + str(self.controlador.comprobar_medios(self.controlador.pista.ruta)[1].sampling_rate)]
		self.lista = wx.ListBox(self.panel, -1, choices= self.lista_datos)
		self.bt_cerrar = wx.Button(self.panel, wx.ID_OK, _('&Cerrar'))

#creación de sizers

		sz1 = wx.BoxSizer(wx.VERTICAL)

		sz1.Add(self.lista, wx.SizerFlags().Expand())
		sz1.Add(self.bt_cerrar)

		self.panel.SetSizer(sz1)

