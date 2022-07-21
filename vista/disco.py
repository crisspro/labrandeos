import wx

import controlador.traductor

class Disco(wx.Dialog):
	def __init__ (self, parent, title, controlador):
		super().__init__(parent, title= title)
		self.Center()
		self.Size = (200,300)
		self.controlador = controlador
		controlador.traductor.Traductor('disco')


		#creación de controles
		panel1 = wx.Panel(self)
		self.l_titulo= wx.StaticText(panel1, -1, _('Título:'))
		self.in_titulo= wx.TextCtrl(panel1, -1, style= wx.TE_PROCESS_ENTER)
		self.in_titulo.SetMaxLength(80)
		self.Bind(wx.EVT_TEXT, self.evento_texto, self.in_titulo)
		self.l_autor= wx.StaticText(panel1, -1, _('Autor:'))
		self.in_autor= wx.TextCtrl(panel1, -1, style= wx.TE_PROCESS_ENTER)
		self.in_autor.SetMaxLength(80)
		self.Bind(wx.EVT_TEXT, self.evento_texto, self.in_autor)
		self.l_fecha= wx.StaticText(panel1, -1, _('Año:'))
		self.in_fecha= wx.TextCtrl(panel1, -1, style= wx.TE_PROCESS_ENTER)
		self.in_fecha.SetMaxLength(4)
		self.Bind(wx.EVT_TEXT, self.admitir_numeros, self.in_fecha)
		self.l_genero= wx.StaticText(panel1, -1, _('Género:'))
		self.in_genero= wx.TextCtrl(panel1, -1, style= wx.TE_PROCESS_ENTER)
		self.in_genero.SetMaxLength(80)
		self.l_comentarios= wx.StaticText(panel1, -1, _('Comentarios:'))
		self.in_comentarios= wx.TextCtrl(panel1, -1, style= wx.TE_MULTILINE|wx.TE_PROCESS_ENTER)
		self.bt_aceptar = wx.Button(panel1, wx.ID_OK, _('&Aceptar'))
		self.bt_aceptar.Enable(False)
		self.bt_aceptar.SetDefault()
		self.bt_cancelar = wx.Button(panel1, wx.ID_CANCEL, _('&Cancelar'))

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

		self.completar_valores()

	def getTitulo(self):
		return self.in_titulo.GetValue()

	def getAutor(self):
		return self.in_autor.GetValue()

	def getFecha(self):
		return self.in_fecha.GetValue()

	def getGenero(self):
		return self.in_genero.GetValue()

	def getComentarios(self):
		return self.in_comentarios.GetValue()

	def evento_texto (self, event):
		self.evalua_llenado()

	def evalua_llenado(self):
		if self.in_autor.GetValue() != '' and self.in_titulo.GetValue() != '':
			self.bt_aceptar.Enable(True)
		else:
			self.bt_aceptar.Enable(False)

	def admitir_numeros(self, event):
		texto = self.in_fecha.GetValue().strip()
		for caracter in texto:
			if caracter.isdigit() == False:
				msg = wx.adv.NotificationMessage(_('Aviso:'), _('Solo se admiten números'), self, wx.ICON_ERROR)
				msg.Show(5)
				self.in_fecha.SetValue('')

	def completar_valores(self):
		if self.controlador.disco != None:
			disco = self.controlador.consultar_disco()
			self.in_titulo.SetValue(disco.titulo)
			self.in_autor.SetValue(disco.autor)
			self.in_fecha.SetValue(disco.fecha)
			self.in_genero.SetValue(disco.genero)
			self.in_comentarios.SetValue(disco.comentarios)

