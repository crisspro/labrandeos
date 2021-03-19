import wx

class Editar(wx.Dialog):
	def __init__(self, parent, title):
		super().__init__(parent, title= title)
		self.Center()
		
		panel1= wx.Panel(self)
		self.l_autor= wx.StaticText(panel1, -1, 'Autor:')
		self.in_autor= wx.TextCtrl(panel1, -1)
		self.in_autor.SetFocus()
		self.l_album= wx.StaticText(panel1, -1, 'Album:')
		self.in_album= wx.TextCtrl(panel1)
		self.l_horas= wx.StaticText(panel1, -1, 'Horas')
		self.in_horas= wx.SpinCtrl(panel1)
		self.in_horas.SetRange(0,24)
		self.l_minutos= wx.StaticText(panel1, -1, 'Minutos')
		self.in_minutos= wx.SpinCtrl(panel1)
		self.in_minutos.SetRange(0,59)
		self.l_segundos= wx.StaticText(panel1, -1, 'Segundos')
		self.in_segundos= wx.SpinCtrl(panel1)
		self.in_segundos.SetRange(0,59)
		self.l_marcos= wx.StaticText(panel1, -1, 'Marcos')
		self.in_marcos= wx.SpinCtrl(panel1)
		self.in_marcos.SetRange(0,74)
		self.bt_reproducir= wx.Button(panel1, -1, '&Reproducir')
		#self.Bind(wx.EVT_BUTTON, Programa.reproducir_pausar, self.bt_reproducir)
		self.bt_aceptar= wx.Button(panel1, wx.ID_OK, '&Aceptar')
		self.bt_cancelar= wx.Button(panel1, wx.ID_CANCEL, '&Cancelar')
