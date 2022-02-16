import wx
import wx.adv


class Editar(wx.Dialog):
	def __init__(self, parent, title, controlador):
		super().__init__(parent, title= title)
		self.Center()
		self.controlador = controlador
		self.tiempo_actual = 0
		self.pista = ''
		self.reproduciendo = False

		# Creación de controles
		self.panel1= wx.Panel(self)
		self.l_titulo = wx.StaticText(self.panel1, -1, 'Título:')
		self.in_titulo= wx.TextCtrl(self.panel1)
		self.in_titulo.SetFocus()
		self.Bind(wx.EVT_TEXT, self.evento_texto, self.in_titulo)
		self.l_autor= wx.StaticText(self.panel1, -1, 'Autor:')
		self.in_autor= wx.TextCtrl(self.panel1, -1)
		self.Bind (wx.EVT_TEXT, self.evento_texto, self.in_autor)
		self.l_horas= wx.StaticText(self.panel1, -1, 'Horas')
		self.in_horas= wx.SpinCtrl(self.panel1)
		self.in_horas.SetRange(0,24)
		self.Bind(wx.EVT_SPINCTRL, self.retomar_tiempo, self.in_horas)
		self.l_minutos= wx.StaticText(self.panel1, -1, 'Minutos')
		self.in_minutos= wx.SpinCtrl(self.panel1)
		self.in_minutos.SetRange(0,59)
		self.Bind(wx.EVT_SPINCTRL, self.retomar_tiempo, self.in_minutos)
		self.l_segundos= wx.StaticText(self.panel1, -1, 'Segundos')
		self.in_segundos= wx.SpinCtrl(self.panel1)
		self.in_segundos.SetRange(0,59)
		self.Bind(wx.EVT_SPINCTRL, self.retomar_tiempo, self.in_segundos)
		self.l_marcos= wx.StaticText(self.panel1, -1, 'Marcos')
		self.in_marcos= wx.SpinCtrl(self.panel1)
		self.in_marcos.SetRange(0,74)
		self.Bind(wx.EVT_SPINCTRL, self.retomar_tiempo, self.in_marcos)
		self.bt_reproducir = wx.Button(self.panel1, -1, '&Reproducir')
		self.Bind (wx.EVT_BUTTON, self.cambiar_etiqueta, self.bt_reproducir)
		self.bt_aceptar= wx.Button(self.panel1, wx.ID_OK, '&Aceptar')
		self.bt_aceptar.Enable(False)
		self.bt_cancelar= wx.Button(self.panel1, wx.ID_CANCEL, '&Cancelar')

#sizers

		sz1 = wx.BoxSizer(wx.VERTICAL)

		sz1.Add(self.l_titulo)
		sz1.Add(self.in_titulo)
		sz1.Add(self.l_autor)
		sz1.Add(self.in_autor)

		sz2 = wx.BoxSizer(wx.HORIZONTAL)

		sz1.Add(sz2)
		sz2.Add(self.l_horas)
		sz2.Add(self.in_horas)
		sz2.Add(self.l_minutos)
		sz2.Add(self.in_minutos)
		sz2.Add(self.l_segundos)
		sz2.Add(self.in_segundos)
		sz2.Add(self.l_marcos)
		sz2.Add(self.in_marcos)

		sz3 = wx.BoxSizer(wx.HORIZONTAL)

		sz1.Add(sz3)
		sz3.Add(self.bt_reproducir)
		sz3.Add(self.bt_aceptar)
		sz3.Add(self.bt_cancelar)

		self.panel1.SetSizer(sz1)

		self.llenar_valores()

# funciones

	def getAutor(self):
		return self.in_autor.GetValue()
	
	def getTitulo(self):
		return self.in_titulo.GetValue()
	
	def getTiempoInicio(self):
		return '{0} horas {1} minutos {2} segundos {3} marcos'.format (self.in_horas.GetValue(), self.in_minutos.GetValue(), self.in_segundos.GetValue(), self.in_marcos.GetValue())

	def alertar(self):
		if self.in_autor.GetValue() == '':
			wx.MessageBox('Debes ingresar un autor.', 'Alerta.')
		elif self.in_titulo.GetValue() == '':
			wx.MessageBox('Debe ingresar un título.', 'Alerta.')

	def getTiempo(self, milesimas):
		self.controlador.temporizar(milesimas)
		tiempo = self.controlador.cargar_tiempo()
		self.in_marcos.SetValue(tiempo[3]) 
		self.in_segundos.SetValue(tiempo[2])
		self.in_minutos.SetValue(tiempo[1])
		self.in_horas.SetValue(tiempo[0])



	def evento_texto (self, event):
		self.evalua_llenado()

	#evalúa el  llenado de los cuadros de edición
	def evalua_llenado(self):
		if self.in_autor.GetValue() != '' and self.in_titulo.GetValue() != '':
			self.bt_aceptar.Enable(True)
		else:
			self.bt_aceptar.Enable(False)

	# cambia la etiqueta del botón reproducir.
	def cambiar_etiqueta(self):
		if self.reproduciendo == True:
			self.bt_reproducir.SetLabel('&Detener')
		else:
			self.bt_reproducir.SetLabel('&Reproducir')

	def retomar_tiempo(self, event):
		tiempo = (self.in_horas.GetValue(), self.in_minutos.GetValue(), self.in_segundos.GetValue(), self.in_marcos.GetValue())
		self.tiempo_actual = self.controlador.reconvertir(tiempo)

	def llenar_valores(self):
		self.in_autor.SetValue(self.controlador.consultar_disco().autor)


class Editar2(Editar):
	def __init__(self, parent, title, controlador):
		super().__init__(parent, title= title, controlador=  controlador)

	def cargar_datos(self, id):
		marca = self.controlador.consultar_datos(id)
		self.in_titulo.SetValue(marca.titulo)
		self.in_autor.SetValue(marca.autor)

