import requests
import requests
import os
import pdb

import accessible_output2.outputs.auto
import pymediainfo
from wx import media
import wx
import wx.adv

import vista.disco
import vista.opciones
from controlador.controlador import Controlador 
from .editar import Editar
from .editar import Editar2
from .acerca_de import Acerca_de


class Programa(wx.Frame):
	def __init__(self, parent, title, controlador):
		super().__init__(parent, title= title)
		self.controlador = controlador
		self.Center()
		self.graficar()
		self.Show()

	#creación de controles
	def graficar(self):
# creación de lector
		self.lector= accessible_output2.outputs.auto.Auto()

		#ID personalizados
		self.id_bt_enfocar_lista = wx.NewIdRef()
		self.id_bt_enfocar_linea_tiempo = wx.NewIdRef()
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
		mn_guardar_proyecto = menu1.Append(-1, '&Guardar proyecto como...')
		self.Bind(wx.EVT_MENU, self.guardar_proyecto, mn_guardar_proyecto)
		mn_generar= menu1.Append(-1, '&Generar CUE')
		self.Bind(wx.EVT_MENU, self.generar, mn_generar)
		salir= menu1.Append(-1, '&Salir')
		self.Bind(wx.EVT_MENU, self.cerrar, salir)

	# creación del menú herramientas
		menu2= wx.Menu()
		herramientas =  barrademenu.Append(menu2,"&Herramientas")
		self.mn_metadatos_disco = menu2.Append(-1, '&Metadatos del álbum')
		self.mn_metadatos_disco.Enable(False)
		self.Bind(wx.EVT_MENU, self.guardar_disco, self.mn_metadatos_disco)
		opciones = menu2.Append(-1, '&Opciones')
		self.Bind(wx.EVT_MENU, self.abrir_opciones, opciones)

	#creación del menú ayuda
		menu3= wx.Menu()
		ayuda= barrademenu.Append(menu3, 'A&yuda')
		manual= menu3.Append(-1, 'Manual')
		self.mn_buscar_actualizacion = menu3.Append(-1, '&Buscar  actualizaciones')
		self.Bind(wx.EVT_MENU, self.buscar_actualizacion, self.mn_buscar_actualizacion)
		acercade= menu3.Append(-1, 'Acerca de')
		self.Bind(wx.EVT_MENU, self.mg_acerca, acercade)


#panel y controles

		panel2= wx.Panel(self)

		l_abrir= wx.StaticText (panel2, -1, 'Carga el archivo de audio que quieres procesar.')
		bt_abrir= wx.Button(panel2, -1, '&Cargar audio')
		self.Bind(wx.EVT_BUTTON, self.abrir_archivo, bt_abrir)
		backend= ''
		self.reproductor= wx.media.MediaCtrl()
		self.reproductor.Create(panel2, style=wx.SIMPLE_BORDER, szBackend=backend)
		self.reproductor.Show(False)


		self.l_encabezado = wx.StaticText(panel2, -1, 'Nuevo proyecto')
		self.font_encabezado =self.l_encabezado.GetFont()
		self.font_encabezado.SetPointSize(30)
		self.l_encabezado.SetFont(self.font_encabezado)
		self.valores= '0:0:0:0'
		self.l_reloj= wx.StaticText(panel2, -1, self.valores)
		self.font_reloj= self.l_reloj.GetFont()
		self.font_reloj.SetPointSize(60)
		self.l_reloj.SetFont(self.font_reloj)
		self.l_pista= wx.StaticText(panel2, -1, 'Línea de tiempo')
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

		self.bt_enfocar_linea_tiempo = wx.Button(panel2, self.id_bt_enfocar_linea_tiempo, 'línea de tiempo')
		self.bt_enfocar_linea_tiempo.Show(False)
		self.Bind(wx.EVT_BUTTON, self.enfocar_linea_tiempo, self.id_bt_enfocar_linea_tiempo)
		self.atajo_enfocar_linea_tiempo = wx.AcceleratorEntry(wx.ACCEL_CTRL, ord ('l'), self.id_bt_enfocar_linea_tiempo)
		self.bt_enfocar_lista = wx.Button(panel2, self.id_bt_enfocar_lista, 'enfocar lista')
		self.bt_enfocar_lista.Show(False)
		self.Bind(wx.EVT_BUTTON, self.enfocar_lista, self.id_bt_enfocar_lista)
		self.atajo_enfocar_lista = wx.AcceleratorEntry(wx.ACCEL_CTRL, ord ('m'), self.id_bt_enfocar_lista)
		self.bt_duracion= wx.Button(panel2, self.id_hablar_duracion, 'Duración')
		self.bt_duracion.Show(False)
		self.Bind(wx.EVT_BUTTON, self.hablar_duracion, self.id_hablar_duracion)
		self.atajo_duracion= wx.AcceleratorEntry(wx.ACCEL_CTRL, ord ('d'), self.id_hablar_duracion)
		self.bt_tiempo_actual= wx.Button(panel2, self.id_bt_tiempo_actual, 'tiempo actual')
		self.bt_tiempo_actual.Show(False)
		self.Bind(wx.EVT_BUTTON, self.hablar_tiempo, self.id_bt_tiempo_actual)
		bt_detener= wx.Button(panel2, -1, '&Detener')
		self.Bind(wx.EVT_BUTTON, self.detener, bt_detener)
		l_volumen= wx.StaticText(panel2, -1, 'Volumen')
		self.volumen= wx.Slider(panel2, -1, 100, 0, 100)
		self.Bind(wx.EVT_SLIDER, self.volumenear,self.volumen)
		self.bt_marcar= wx.Button(panel2, -1, '&Marcar')
		self.bt_marcar.Enable(False)
		self.Bind(wx.EVT_BUTTON, self.marcar, self.bt_marcar)
		self.atajo_tiempo_actual= wx.AcceleratorEntry(wx.ACCEL_CTRL, ord ('t'), self.id_bt_tiempo_actual)
		self.entradas_atajos= [self.atajo_enfocar_lista, self.atajo_enfocar_linea_tiempo, self.atajo_tiempo_actual, self.atajo_duracion]
		self.tabla_atajos= wx.AcceleratorTable(self.entradas_atajos)
		self.SetAcceleratorTable(self.tabla_atajos)

		self.Bind(wx.EVT_CLOSE, self.cerrar)
# Construcción de lista
		self.l_lista = wx.StaticText(panel2, -1, 'Marcas')
		self.lista= wx.ListCtrl(panel2, -1,style= wx.LC_REPORT)
		self.lista.InsertColumn(0, 'N°')
		self.lista.InsertColumn(1, 'Título')
		self.lista.InsertColumn(2, 'Autor')
		self.lista.InsertColumn(3, 'Tiempo de inicio')
		self.Bind(wx.EVT_LIST_KEY_DOWN, self.detectar_tecla, self.lista)
		self.Bind(wx.EVT_LIST_ITEM_RIGHT_CLICK, self.desplegar_menu, self.lista)
		self.Bind(wx.EVT_LIST_ITEM_FOCUSED, self.posicionar_marca, self.lista)
		self.bt_editar = wx.Button(panel2, -1, '&Editar')
		self.Bind(wx.EVT_BUTTON, self.abrir_editar2, self.bt_editar)
		self.bt_generar= wx.Button(panel2, -1, '&GENERAR CUE')
		self.Bind(wx.EVT_BUTTON, self.generar, self.bt_generar)



#estado de los controles
		self.bt_generar.Enable(True)
		bt_abrir.SetFocus() #pone el foco del cursor al abrir la aplicación.

#creación de sizers

		sz1= wx.BoxSizer(wx.VERTICAL)

		sz1.Add(self.l_encabezado, wx.SizerFlags().Center())
		sz1.Add(l_abrir)
		sz1.Add(bt_abrir)
		sz1.Add(self.l_reloj, wx.SizerFlags().Center())
		sz1.Add(self.reproductor)

		sz1.Add(self.pista, wx.SizerFlags().Expand())


		sz2= wx.BoxSizer(wx.HORIZONTAL)
		sz1.Add(sz2)
		sz2.Add(self.bt_reproducir)
		sz2.Add(bt_detener)
		sz2.Add(self.volumen)
		sz2.Add(self.bt_marcar)

		sz1.Add(self.lista, wx.EXPAND|wx.RIGHT)
		sz1.Add(self.bt_editar)
		sz1.Add(self.bt_generar)

		panel2.SetSizer (sz1)




	# carga marcas en  la lista
	def listar(self):
		id = self.lista.GetItemCount()
		for marca in self.controlador.getMarcas():
			self.lista.InsertStringItem(id, str(marca.id))
			self.lista.SetStringItem(id, 1,  marca.titulo)
			self.lista.SetStringItem(id, 2, marca.autor)
			self.lista.SetStringItem(id, 3,marca.tiempo_inicio)
			id+=1

	def refrescar_lista(self):
		self.lista.DeleteAllItems()
		self.listar()

	def detectar_tecla(self, event):
		tecla = event.GetKeyCode()
		if tecla == wx.WXK_DELETE:
			self.borrar_item(None)

	def posicionar_marca(self, event):
		item = self.lista.GetFocusedItem()
		marca =self.controlador.getMarcas()[item]
		self.reproductor.Seek(marca.milesimas)

	def borrar_item(self, event):
		item = self.lista.GetFocusedItem()
		self.controlador.borrar_marca(item)
		self.lista.DeleteItem(item)
		self.lector.output('Eliminada')

	def desplegar_menu(self, event):
		item = self.lista.GetFocusedItem()
		menu = wx.Menu()
		editar = wx.MenuItem(menu, -1, '&Editar')
		menu.AppendItem(editar)
#		self.lista.PopupMenu(menu)


	def cerrar (self, event):
		if os.path.exists('temp.proyecto.cgp'):
			resp = wx.MessageBox('Estás a punto de cerrar el programa. Los cambios que hayas echo al proyecto no se guardarán. \n ¿Deseas salir?', 'Advertencia.', style= wx.YES_NO|wx.NO_DEFAULT| wx.ICON_WARNING)
			if resp == wx.YES:
				self.controlador.limpiar_temporal()
				self.Destroy()
		else:
			self.Destroy()

	def guardar_disco(self, event):
		self.vn_disco = vista.disco.Disco(self, 'Metadatos del álbum', self.controlador)
		if self.vn_disco.ShowModal() == wx.ID_OK:
			self.controlador.crear_disco(self.vn_disco.getTitulo(),
			self.vn_disco.getAutor(),
			self.vn_disco.getFecha(),
			self.vn_disco.getGenero(),
			self.vn_disco.getComentarios())
			self.mn_metadatos_disco.Enable(True)
			self.l_encabezado.SetLabel(self.controlador.consultar_disco().titulo + ' - ' + self.controlador.consultar_disco(). autor)



	def abrir_archivo (self, event):
		self.dialogo= wx.FileDialog(self, 'Abrir archivo', style=wx.FD_OPEN)
		if self.dialogo.ShowModal() == wx.ID_OK:
			archivo_info= pymediainfo.MediaInfo.parse(self.dialogo.GetPath())
			self.path= ''
			for track in archivo_info.tracks:
				if track.track_type == 'Audio':
					self.path= self.dialogo.GetPath()
					self.bt_marcar.Enable(True)
				elif track.track_type == 'Video':
					self.path= ''
					break
			if self.path == '':
				wx.MessageBox('No es posible cargar el fichero, sólo se admiten archivos de audio.', caption= 'Atención.', style= wx.ICON_ERROR)
			self.reproductor.Load(self.path)
			self.bt_reproducir.SetFocus()
			self.controlador.ruta_audio = self.path
			self.guardar_disco(None)

	#abre un proyecto existente
	def abrir_proyecto(self, event):
		self.dialogo_abrir_proyecto = wx.FileDialog(self, 'Abrir proyecto', style=wx.FD_OPEN, wildcard= '*.CGP')
		if self.dialogo_abrir_proyecto.ShowModal() == wx.ID_OK:
			if self.controlador.ruta_proyecto != self.dialogo_abrir_proyecto.GetPath():
				mensaje = wx.MessageBox('Estás a punto de abrir un nuevo proyecto. Los cambios que hayas hecho se perderán. \n ¿Deseas continuar de todos modos?', 'Advertencia.', style= wx.YES_NO| wx.NO_DEFAULT| wx.ICON_WARNING)
				if mensaje == 2:
					self.controlador.ruta_proyecto = self.dialogo_abrir_proyecto.GetPath()
					self.controlador.limpiar_temporal()
					self.controlador.load()
					self.listar()


	#guarda el proyecto en una ruta específica
	def guardar_proyecto(self, event):
		self.dialogo_guardar = wx.FileDialog(self, 'Guardar proyecto', style=wx.FD_SAVE, wildcard= '*.CGP')
		if self.dialogo_guardar.ShowModal() == wx.ID_OK:
			self.controlador.ruta_proyecto = self.dialogo_guardar.GetPath()
			self.controlador.save()
			self.controlador.limpiar_temporal()

	#abre la ventana de opciones
	def abrir_opciones(self, event):
		vn_opciones = vista.opciones.Opciones(self, 'Opciones')
		if vn_opciones.ShowModal() == wx.ID_OK:
			vn_opciones.guardar_opciones()


	#busca actualizaciones
	def buscar_actualizacion(self, event):
		self.controlador.verificarNuevaVersion()
		if self.controlador.actualizado == True:
			wx.MessageBox('No hay ninguna nueva versión disponible', 'Aviso.')


# muestra información acerca del programa
	def mg_acerca(self, event):
		dlg = Acerca_de(self, title= 'Acerca de...')
		if dlg.ShowModal() == wx.ID_OK:
			dlg.close()

	def enfocar_linea_tiempo(self, event):
		self.pista.SetFocus()

	def enfocar_lista(self, event):
		self.lista.SetFocus()

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

#pausa la reproducción
	def pausar(self, event):
		self.estado= self.reproductor.GetState()
		if self.estado == 2:
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

	#reproduce y pausa en ventana editar.
	def reproducir_editar(self, event):
		self.reproductor.Seek(self.editar.tiempo_actual)
		self.reproducir_pausar(None)
		if self.estado == 1 or self.estado == 0:
			self.editar.reproduciendo = True
		else:
			self.editar.reproduciendo = False
		self.editar.cambiar_etiqueta()

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
		self.lector.output(str(self.horas) + 'horas' + str(self.minutos) + 'minutos' + str(self.segundos) + 'segundos' + str(self.marcos) + 'marcos' + ' en tiempo actual')

# verbaliza el tiempo de duración del archivo de audio.
	def hablar_duracion (self, event):
		self.duracion= self.reproductor.Length()
		valores= self.calcular_tiempo(self.duracion)
		self.lector.output('Duración de la pista. ' + str(valores[0]) + 'horas' + str(valores [1]) + 'minutos' + str(valores [2]) + 'segundos' + str(valores [3]) + 'marcos')

	def marcar (self, event):
		self.reproductor.Pause()
		self.bt_reproducir.SetLabel('&Reproducir')
		wx.adv.Sound.PlaySound( os.path.join('files', 'sounds', 'marca.wav'))
		self.lector.output('Marcado')
		self.vn_editar()


	def vn_editar(self):
		self.editar = Editar(self, 'Crear marca', self.controlador)
		self.editar.getTiempo(self.reproductor.Tell())
		self.editar.tiempo_actual = self.reproductor.Tell()
		self.editar.pista = self.path
		self.editar.Bind(wx.EVT_BUTTON, self.reproducir_editar, self.editar.bt_reproducir)
		if self.editar.ShowModal() == wx.ID_OK:
			self.pausar(None)
			marca = self.controlador.crearMarca(self.lista.GetItemCount(),
				self.editar.getTitulo(),
				self.editar.getAutor(),
				self.editar.getTiempoInicio(),
				self.editar.tiempo_actual)
			id=self.lista.GetItemCount()
			self.lista.InsertStringItem(id,  str(marca.id))
			self.lista.SetStringItem(id, 1, marca.titulo)
			self.lista.SetStringItem(id, 2, marca.autor)
			self.lista.SetStringItem(id, 3, marca.tiempo_inicio)
			self.refrescar_lista()
		else:
			self.pausar(None)

	def abrir_editar2(self,event):
		self.editar2 = Editar2(self, 'Editar marca')
		item = self.lista.GetFocusedItem()
		self.editar2.cargar_datos(item)
		if self.editar2.ShowModal() == wx.ID_OK:
			pass

	def generar(self, event):
		self.controlador.generar_cue()
		wx.adv.Sound.PlaySound( os.path.join('files', 'sounds', 'ok.wav'))




#Creación de instancias

controlador = Controlador()