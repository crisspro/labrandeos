import pdb
import wx
from controlador.traductor import Traductor


class Informacion_medios(wx.Dialog):
	def __init__(self, parent, title, controlador):
		super().__init__(parent, title= title)
		self.Center()
		Traductor('informacion_medios')
		self.controlador = controlador
		self.controlador.tiempo.convertir(self.controlador.pista.duracion)

		self.panel = wx.Panel(self)
		self.lista_datos = [_('Fichero: ') + self.controlador.pista.nombre + self.controlador.pista.extencion,
		_('Duración: ') + str(self.controlador.tiempo.horas) + _('horas ') + str(self.controlador.tiempo.minutos) + _('minutos ') + str(self.controlador.tiempo.segundos) + _('segundos ') + str(self.controlador.tiempo.marcos) + _('marcos'),
		_('Formato: ') + self.controlador.comprobar_medios(self.controlador.pista.ruta)[1].get('format'),
		_('Tasa de bits: ') + str(self.controlador.comprobar_medios(self.controlador.pista.ruta)[1].get('other_bit_rate')),
		_('Modo de taza de bits: ') + str(self.controlador.comprobar_medios(self.controlador.pista.ruta)[1].get('bit_rate_mode')),
		_('Velocidad de muestreo: ') + str(self.controlador.comprobar_medios(self.controlador.pista.ruta)[1].get('sampling_rate')),
		_('Canales: ' + str(self.controlador.comprobar_medios(self.controlador.pista.ruta)[1].get('channel_s')))]
		self.lista = wx.ListBox(self.panel, -1, choices= self.lista_datos)
		self.bt_cerrar = wx.Button(self.panel, wx.ID_OK, _('&Cerrar'))

#creación de sizers

		sz1 = wx.BoxSizer(wx.VERTICAL)

		sz1.Add(self.lista, wx.SizerFlags().Expand())
		sz1.Add(self.bt_cerrar)

		self.panel.SetSizer(sz1)

