#título: CUE Genesis
#autor: Crisspro
#lisencia: GPL-3.0

import requests
import os
import webbrowser

import accessible_output2.outputs.auto
import pymediainfo
from wx import media
import wx
import wx.adv

from .config import *
from controlador import Controlador 
from .editar import Editar





class Programa(wx.Frame):
	def __init__(self, parent, title, controlador):
		super().__init__(parent, title= title)
		self.controlador = controlador
		self.Center()
		self.graficar()
		self.Show()




	def verificarNuevaVersion(self):
		try:
			link= 'https://api.github.com/repos/crisspro/cuegenesis/releases/latest'
			coneccion= requests.get(link, timeout= 5)
		except(requests.ConectionError, requests.Timeout):
			print('No hay conección')
		else:
			print('Hay conección')
			v= coneccion.json() ['tag_name']
			if v != version_app:
				wx.adv.Sound.PlaySound(os.path.join('sounds', 'nueva_version.wav'))
				resp= wx.MessageBox('Hay disponible una nueva versión de ' + nombre_app + '(' + v + ')' + '. ¿Quieres descargarla ahora?', caption= 'Aviso', style= wx.YES_NO)
				if resp == wx.YES:
					dw= coneccion.json() ['assets']
					for i in dw:
						dw= i['browser_download_url']
					webbrowser.open(dw)
					self.Close()
	
	#creación de controles
	def graficar(self):
# creación de lector
		self.lector= accessible_output2.outputs.auto.Auto()
		
		# verifica si hay nueva versión del programa.
		#self.verificarNuevaVersion()
		
		#ID personalizados
		self.id_bt_marcar= wx.NewIdRef()
		self.id_bt_detener= wx.NewIdRef()
		self.id_bt_reproducir= wx.NewIdRef()
		self.id_bt_tiempo_actual= wx.NewIdRef()
		self.id_hablar_duracion= wx.NewIdRef()


# creacion de la barra de menu.
		barrademenu= wx.MenuBar()
		self.SetMenuBar(barrademenu)

	#creación del menú archivo
		menu1= wx.Menu()
		archivo= barrademenu.Append(menu1,"&Archivo")
		nuevo= menu1.Append(-1, '&Nuevo')
		mn_cargar_audio = menu1.Append(-1, '&Cargar audio')
		self.Bind(wx.EVT_MENU, self.abrir_archivo, mn_cargar_audio)
		mn_abrir_proyecto = menu1.Append(-1, '&Abrir proyecto')
		self.Bind(wx.EVT_MENU, self.abrir_proyecto, mn_abrir_proyecto)
		mn_guardar_proyecto = menu1.Append(-1, '&Guardar proyecto')
		self.Bind(wx.EVT_MENU, self.guardar_proyecto, mn_guardar_proyecto)
		mn_generar= menu1.Append(-1, '&Generar CUE')
		self.Bind(wx.EVT_MENU, self.generar, mn_generar)
		salir= menu1.Append(-1, '&Salir')
		self.Bind(wx.EVT_MENU, self.cerrar, salir)

	#creación del menú ayuda
		menu2= wx.Menu()
		ayuda= barrademenu.Append(menu2, 'A&yuda')
		manual= menu2.Append(-1, 'Manual')
		acercade= menu2.Append(-1, 'Acerca de')
		self.Bind(wx.EVT_MENU, self.mg_acerca, acercade)


#panel y controles
		panel2= wx.Panel(self)

		l_abrir= wx.StaticText (panel2, -1, 'Carga el archivo de audio que quieres procesar.')
		bt_abrir= wx.Button(panel2, -1, '&Cargar audio')
		self.Bind(wx.EVT_BUTTON, self.abrir_archivo, bt_abrir)
		self.l_instrucciones= wx.StaticText (panel2, -1, 'ingresa los metadatos  a continuación.') 
		l_autor= wx.StaticText(panel2, -1, 'Autor:')
		self.in_autor= wx.TextCtrl(panel2, -1)
		self.in_autor.SetMaxLength(80)
		l_album= wx.StaticText(panel2, -1, 'Título del álbum:')
		self.in_album= wx.TextCtrl(panel2, -1)
		self.in_album.SetMaxLength(80)
		l_fecha= wx.StaticText(panel2, -1, 'Año:')
		self.in_fecha= wx.TextCtrl(panel2, -1)
		self.in_fecha.SetMaxLength(4)
		l_genero= wx.StaticText(panel2, -1, 'Género:')
		self.in_genero= wx.TextCtrl(panel2, -1)
		self.in_genero.SetMaxLength(80)
		l_comentarios= wx.StaticText(panel2, -1, 'Comentarios:')
		self.in_comentarios= wx.TextCtrl(panel2, -1, style= wx.TE_MULTILINE)
		backend= ''
		self.reproductor= wx.media.MediaCtrl()
		self.reproductor.Create(panel2, style=wx.SIMPLE_BORDER, szBackend=backend)
		self.reproductor.Show(False)


		bt_generar= wx.Button(panel2, -1, '&Generar CUE')
		self.Bind(wx.EVT_BUTTON, self.generar, bt_generar)
		self.valores= '0:0:0:0'
		self.l_reloj= wx.StaticText(panel2, -1, self.valores)
		self.font_reloj= self.l_reloj.GetFont()
		self.font_reloj.SetPointSize(60)
		self.l_reloj.SetFont(self.font_reloj)
		self.l_pista= wx.StaticText(panel2, -1, 'Pista')
		self.minutaje= 1
		self.pista= wx.Slider(panel2, -1, 0, 0, self.minutaje,size= (400, -1))
		self.pista.SetLineSize(5000)
		self.pista.SetPageSize(60000)

		self.Bind(wx.EVT_SLIDER, self.mover, self.pista)		
		self.bt_reproducir= wx.Button(panel2, -1, '&Reproducir')
		self.Bind(wx.EVT_BUTTON, self.reproducir_pausar, self.bt_reproducir)
		self.Bind(wx.media.EVT_MEDIA_STOP, self.detener, self.reproductor)
		self.timer= wx.Timer(self)
		self.timer.Start(self.reproductor.Length())
		self.Bind(wx.EVT_TIMER, self.temporizar)



		self.bt_duracion= wx.Button(panel2, self.id_hablar_duracion, 'Duración')
		self.bt_duracion.Show(False)
		self.Bind(wx.EVT_BUTTON, self.hablar_duracion, self.id_hablar_duracion)
		self.atajo_duracion= wx.AcceleratorEntry(wx.ACCEL_CTRL, ord ('d'), self.id_hablar_duracion)
		self.bt_tiempo_actual= wx.Button(panel2, self.id_bt_tiempo_actual, 'tiempo actual')
		self.bt_tiempo_actual.Show(False)
		self.Bind(wx.EVT_BUTTON, self.hablar_tiempo, self.id_bt_tiempo_actual)
		bt_detener= wx.Button(panel2, self.id_bt_detener, '&Detener')
		self.Bind(wx.EVT_BUTTON, self.detener, self.id_bt_detener)
		self.atajo_detener= wx.AcceleratorEntry(wx.ACCEL_CTRL, ord ('s'), self.id_bt_detener)
		l_volumen= wx.StaticText(panel2, -1, 'Volumen')
		self.volumen= wx.Slider(panel2, -1, 100, 0, 100)
		self.Bind(wx.EVT_SLIDER, self.volumenear,self.volumen)
		self.bt_marcar= wx.Button(panel2, self.id_bt_marcar, '&Marcar')
		self.Bind(wx.EVT_BUTTON, self.marcar, self.id_bt_marcar)
		self.atajo_marcar= wx.AcceleratorEntry(wx.ACCEL_CTRL, ord ('m'), self.id_bt_marcar)
		self.atajo_tiempo_actual= wx.AcceleratorEntry(wx.ACCEL_CTRL, ord ('t'), self.id_bt_tiempo_actual)
		self.entradas_atajos= [self.atajo_marcar, self.atajo_detener, self.atajo_tiempo_actual, self.atajo_duracion]
		self.tabla_atajos= wx.AcceleratorTable(self.entradas_atajos)
		self.SetAcceleratorTable(self.tabla_atajos)

# Construcción de lista
		self.lista= wx.ListCtrl(panel2, -1, style= wx.LC_REPORT)
		self.lista.InsertColumn(0, 'Título')
		self.lista.InsertColumn(1, 'Autor')
		# cargamos marcas:
		id = self.lista.GetItemCount()
		for marca in self.controlador.getMarcas():
			self.lista.InsertStringItem(id, marca.titulo)
			self.lista.SetStringItem(id, 1, marca.autor)
			id+=1
		

#estado de los controles
		bt_generar.Enable(True)
		l_abrir.SetFocus() #pone el foco del cursor al abrir la aplicación.

#creación de sizers

		sz1= wx.BoxSizer(wx.VERTICAL)

		sz1.Add(l_abrir)
		sz1.Add(bt_abrir)
		sz1.Add(self.l_instrucciones)
		sz1.Add(l_autor)
		sz1.Add(self.in_autor)
		sz1.Add(l_album)
		sz1.Add(self.in_album)
		sz1.Add(l_fecha)
		sz1.Add(self.in_fecha)
		sz1.Add(l_genero)
		sz1.Add(self.in_genero)
		sz1.Add(l_comentarios)
		sz1.Add(self.in_comentarios)
		sz1.Add(self.reproductor)
		sz1.Add(bt_generar)
		sz1.Add(self.l_reloj)
		sz1.Add(self.pista)


		sz2= wx.BoxSizer(wx.HORIZONTAL)
		sz1.Add(sz2)
		sz2.Add(self.bt_reproducir)
		sz2.Add(bt_detener)
		sz2.Add(self.volumen)
		sz2.Add(self.bt_marcar)

		sz1.Add(self.lista, wx.EXPAND|wx.RIGHT)

		panel2.SetSizer (sz1)


# arma la lista	def listar (self, event):
	pass


	def generar (self, event):
		if self.in_autor.GetValue() == '' and self.in_album.GetValue() == '':
			nombre_cue= 'Sin autor - Nuevo disco.cue'
			archivo= open( os.path.join(self.dialogo.GetDirectory(), nombre_cue), 'w+')
		elif self.in_autor.GetValue() == '':
			nombre_cue= ('Sin autor - ' + self.in_album.GetValue() + '.cue')
			archivo= open(os.path.join(self.dialogo.GetDirectory(), nombre_cue), 'w+')
		elif self.in_album.GetValue() == '':
			nombre_cue= (self.in_autor.GetValue() + ' - Nuevo disco.cue')
			archivo= open(os.path.join(self.dialogo.GetDirectory(), nombre_cue), 'w+')
		else:
			nombre_cue= (self.in_autor.GetValue() + ' - ' + self.in_album.GetValue() + '.cue')
			archivo= open( os.path.join(self.dialogo.GetDirectory(), nombre_cue), 'w+')
		if self.in_autor.GetValue() != '':
			archivo.write("TITLE "+'"' + self.in_album.GetValue() + '"' + "\n")
		if self.in_album.GetValue() != '':
			archivo.write("PERFORMER " + '"' + self.in_autor.GetValue() + '"' + "\n")
		if self.in_fecha.GetValue() != '':
			archivo.write("REM DATE " + str (self.in_fecha.GetValue()) + "\n")
		if self.in_genero.GetValue() != '':
			archivo.write("REM GENRE " + '"' + self.in_genero.GetValue() + '"' + "\n")
		if self.in_comentarios.GetValue() != '':
			archivo.write("REM COMMENT 		" + '"' + self.in_comentarios.GetValue() + '"' + "\n")
		archivo.write("FILE " + '"' +self.dialogo.GetFilename() + '"' + " ")
		archivo.close()
		if os.path.isfile(os.path.join(self.dialogo.GetDirectory(), nombre_cue)):
			wx.adv.Sound.PlaySound(os.path.join('sounds', 'ok.wav'))
			resp= wx.MessageBox('El archivo "CUE" ha sido guardado con éxito. ¿Deseas abrir la carpeta de destino?', caption= 'Listo', style= wx.YES_NO)
			if resp == wx.YES:
				os.startfile(self.dialogo.GetDirectory())
		else:
			wx.MessageBox('Ha ocurrido un error. No se ha podido guardar el archivo CUE.', caption= 'Mensaje', style= wx.ICON_ERROR)

	def cerrar (self, event):
		self.Close()

	def abrir_archivo (self, event):
		self.dialogo= wx.FileDialog(self, 'Abrir archivo', style=wx.FD_OPEN)
		if self.dialogo.ShowModal() == wx.ID_OK:
			archivo_info= pymediainfo.MediaInfo.parse(self.dialogo.GetPath())
			self.path= ''
			for track in archivo_info.tracks:
				if track.track_type == 'Audio':
					self.path= self.dialogo.GetPath()
				elif track.track_type == 'Video':
					self.path= ''
					break
			if self.path == '':
				wx.MessageBox('No es posible cargar el fichero, sólo se admiten archivos de audio.', caption= 'Mensaje', style= wx.ICON_ERROR)
			self.reproductor.Load(self.path)
			self.l_instrucciones.SetFocus()

	#abre un proyecto existente
	def abrir_proyecto(self, event):
		self.dialogo_abrir_proyecto = wx.FileDialog(self, 'Abrir proyecto', style=wx.FD_OPEN, wildcard= '*.CGP')
		if self.dialogo_abrir_proyecto.ShowModal() == wx.ID_OK:
			if self.controlador.ruta_proyecto != self.dialogo_abrir_proyecto.GetPath():
				mensaje = wx.MessageBox('Estás a punto de abrir un nuevo proyecto. Los cambios que hayas hecho se perderán. \n ¿Deseas continuar de todos modos?', 'Advertencia', style= wx.YES_NO)
				if mensaje == wx.ID_OK:
					self.controlador.ruta_proyecto = self.dialogo_abrir_proyecto.GetPath()
					self.controlador.load()


	#guarda el proyecto en una ruta específica
	def guardar_proyecto(self, event):
		self.dialogo_guardar = wx.FileDialog(self, 'Guardar proyecto', style=wx.FD_SAVE, wildcard= '*.CGP')
		if self.dialogo_guardar.ShowModal() == wx.ID_OK:
			self.controlador.ruta_proyecto = self.dialogo_guardar.GetPath()
			self.controlador.save()
 




# muestra información acerca del programa
	def mg_acerca(self, event):
		wx.MessageBox('Versión: ' + version_app + '\n' + 'autor: ' + autor_app + '\n' + 'Licencia: ' + lisencia_app, caption= 'Acerca de ' + nombre_app)

# reproduce o pausa la pista.
	def reproducir_pausar (self, event):
		self.estado= self.reproductor.GetState()
		if self.estado == 1 or self.estado == 0:
			self.reproductor.Play()
			self.bt_reproducir.SetLabel('&Pausar')
			self.minutaje= self.reproductor.Length()
			self.pista.SetMax(self.minutaje)
		elif self.estado == 2:
			self.reproductor.Pause()
			self.bt_reproducir.SetLabel('&Reproducir')

# detiene la reproducción
	def detener (self, event):
		self.estado= self.reproductor.GetState()
		if self.estado == 1 or self.estado == 2:
			self.reproductor.Stop()
			self.bt_reproducir.SetLabel('&Reproducir')
		else:
			self.bt_reproducir.SetLabel('&Reproducir')

# controla el volumen
	def volumenear (self, event):
		a= self.volumen.GetValue()
		b= a /100
		self.reproductor.SetVolume(b)

#busca un momento de la pista cuando el usuario mueve la aguja del control
	def mover (self, event):
		self.reproductor.Seek(self.pista.GetValue())



#mueve la aguja del control de la pista de forma automática a medida que se reproduce el audio
	def temporizar (self, event):
		self.tiempo= self.reproductor.Tell()
		self.pista.SetValue(self.tiempo)
		valores= self.calcular_tiempo(self.tiempo)
		str_valores= []
		for i in valores:
			v= str(i)
			c_v= len(v)
			if c_v == 1:
				v= '0'+v
			str_valores.append(v)
		valores= ' : '.join(str_valores)
		self.l_reloj.SetLabel(valores)

# calcula y muestra el tiempo de la pista en horas,minutos,segundos y marcos.
	def calcular_tiempo (self, tiempo):
		milesimas= int(tiempo*75/1000) #convierte milésimas a cantidad de marcos
		self.marcos= milesimas%75 
		self.segundos= int(milesimas/75%60)
		self.minutos= int(milesimas/60/75%60)
		self.full_minutos= int(milesimas/60/75)
		self.horas= int(milesimas/60/60/75)
		self.valores= (self.horas, self.minutos, self.segundos, self.marcos)
		return self.valores
# verbaliza el tiempo actual de reproducción
	def hablar_tiempo (self, event):
		self.lector.output(str(self.horas) + 'horas' + str(self.minutos) + 'minutos' + str(self.segundos) + 'segundos' + str(self.marcos) + 'marcos')

# verbaliza el tiempo de duración del archivo de audio.
	def hablar_duracion (self, event):
		self.duracion= self.reproductor.Length()
		valores= self.calcular_tiempo(self.duracion)
		self.lector.output('Duración. ' + str(valores[0]) + 'horas' + str(valores [1]) + 'minutos' + str(valores [2]) + 'segundos' + str(valores [3]) + 'marcos')

	def marcar (self, event):
		self.reproductor.Pause()
		wx.adv.Sound.PlaySound( os.path.join('sounds', 'marca.wav'))
		self.lector.output('Marcado')
		self.vn_editar()

	def vn_editar(self):
		dlg = Editar(self, title= 'Editar')
		if dlg.ShowModal() == wx.ID_OK:
			marca = self.controlador.crearMarca(dlg.getTitulo(),
				dlg.getAutor(),
				dlg.getTiempoInicio())
			self.lista.Append(str(marca))
			

# lista las marcas en el control lista.
	def listar (self, event):
		for i in Pista.lista:
			print(i)

