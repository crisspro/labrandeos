import wx
import controlador.configuracion


class Acerca_de(wx.Dialog):
	def __init__(self, parent, title):
		super().__init__(parent, title= title)
		self.Center()
		panel = wx.Panel(self)
		self.in_info = wx.TextCtrl(panel, -1, controlador_app.nombre_app + ' ' + controlador_app.version_app + '\n' + _('Autor: ') + controlador_app.autor_app + '\n' + _('Licencia: ') + controlador_app.licencia_app, style= wx.TE_MULTILINE|wx.TE_READONLY)
		self.bt_visitar = wx.Button(panel, -1, _('&Visitar sitio del proyecto'))
		self.Bind(wx.EVT_BUTTON, self.visitar_sitio, self.bt_visitar)
		self.bt_cerrar = wx.Button(panel, wx.ID_OK, _('&Cerrar'))

#creación de sizers

		sz1 = wx.BoxSizer(wx.VERTICAL)

		sz1.Add(self.in_info, wx.SizerFlags().Expand())
		sz1.Add(self.bt_visitar)
		sz1.Add(self.bt_cerrar)

		panel.SetSizer(sz1)

#Funciones

	def visitar_sitio(self, event):
		wx.LaunchDefaultBrowser(controlador_app.sitio_app)

controlador_app = controlador.configuracion.App()