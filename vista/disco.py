import wx

class Disco(wx.Dialog):
	def __init__ (self, parent, title):
		super().__init__(parent, title= title)
		self.Center()
		self.Size = (200,300)

		panel1 = wx.Panel(self)
		self.l_titulo= wx.StaticText(panel1, -1, 'Título:')
		self.in_titulo= wx.TextCtrl(panel1, -1)
		self.in_titulo.SetMaxLength(80)
		self.l_autor= wx.StaticText(panel1, -1, 'Autor:')
		self.in_autor= wx.TextCtrl(panel1, -1)
		self.in_autor.SetMaxLength(80)
		self.l_fecha= wx.StaticText(panel1, -1, 'Año:')
		self.in_fecha= wx.TextCtrl(panel1, -1)
		self.in_fecha.SetMaxLength(4)
		self.l_genero= wx.StaticText(panel1, -1, 'Género:')
		self.in_genero= wx.TextCtrl(panel1, -1)
		self.in_genero.SetMaxLength(80)
		self.l_comentarios= wx.StaticText(panel1, -1, 'Comentarios:')
		self.in_comentarios= wx.TextCtrl(panel1, -1, style= wx.TE_MULTILINE)
		self.bt_aceptar = wx.Button(panel1, wx.ID_OK, '&Aceptar')
		self.bt_cancelar = wx.Button(panel1, wx.ID_CANCEL, '&Cancelar')

# creación de sizers

		sz1 = wx.BoxSizer(wx.VERTICAL)
		sz1.Add(self.l_titulo)
		sz1.Add(self.in_titulo)
		sz1.Add(self.l_autor)
		sz1.Add(self.in_autor)
		sz1.Add(self.l_fecha)
		sz1.Add(self.in_fecha)
		sz1.Add(self.l_genero)
		sz1.Add(self.in_genero)
		sz1.Add(self.l_comentarios)
		sz1.Add(self.in_comentarios)

		sz2 = wx.BoxSizer(wx.HORIZONTAL)
		sz1.Add(sz2)
		sz2.Add(self.bt_aceptar)
		sz2.Add(self.bt_cancelar)

		panel1.SetSizer(sz1)