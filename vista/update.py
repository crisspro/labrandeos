import wx

class Update(wx.Dialog):
	def __init__(self, parent, title, mensaje, maximo):
		wx.Dialog.__init__(self, parent, title= title)
		self.dlg_progreso = wx.Gauge(self, range=maximo)
		self.Show()
		self.bt_cancelar = wx.Button(self, -1,  '&Cancelar')
		self.Bind(wx.EVT_BUTTON, self.cancelar, self.bt_cancelar)

		self.sz1 = wx.BoxSizer(wx.VERTICAL)
		
		self.sz1.Add( self.dlg_progreso, 0, wx.EXPAND|wx.ALL, 10)
		self.sz1.Add(self.bt_cancelar, 0, wx.ALIGN_CENTER|wx.ALL, 10)
		self.SetSizer(self.sz1)
		self.Layout()
		self.cancelado = False

	def cancelar(self, event):
		self.cancelado = True
		self.Destroy()
		self.Destroy()

app = wx.App()
Update(None, 'Descarga', 'Descargando Labrandeos...', maximo= 100)
app.MainLoop()