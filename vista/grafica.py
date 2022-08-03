import pdb
import os

import accessible_output2.outputs.auto
import pymediainfo
import requests
from wx import media
import wx
import wx.adv

import vista.disco
import vista.opciones
from controlador.controlador import Controlador
from controlador.traductor import Traductor 
from .editar import Editar
from .editar import Editar2
from .acerca_de import Acerca_de


class Programa(wx.Frame):
	def __init__(self, parent, title, controlador, app, opciones):
		super().__init__(parent, title= title, style = wx.DEFAULT_FRAME_STYLE|wx.MAXIMIZE)
		self.syze = (800,800)
		self.controlador = controlador
		self.controlador_app = app
		self.controlador_opciones = opciones
		self.Center()
		self.graficar()
		self.Show()

	#creación de controles
	def graficar(self):
		Traductor('grafica')
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
		archivo = barrademenu.Append(menu1, _('&Archivo'))
		self.mn_nuevo_proyecto = menu1.Append(-1, _('&Nuevo proyecto'))
		self.mn_nuevo_proyecto.Enable(False)
		self.Bind(wx.EVT_MENU, self.crear_proyecto, self.mn_nuevo_proyecto)
		self.mn_cargar_audio = menu1.Append(-1, _('&Cargar audio'))
		self.Bind(wx.EVT_MENU, self.abrir_archivo, self.mn_cargar_audio)
		self.mn_abrir_proyecto = menu1.Append(-1, _('&Abrir proyecto'))
		self.Bind(wx.EVT_MENU, self.abrir_proyecto, self.mn_abrir_proyecto)
		self.mn_guardar_proyecto = menu1.Append(-1, _('&Guardar proyecto como...'))
		self.mn_guardar_proyecto.Enable(False)

		self.Bind(wx.EVT_MENU, self.guardar_proyecto, self.mn_guardar_proyecto)
		self.mn_generar = menu1.Append(-1, _('&Generar CUE'))
		self.mn_generar.Enable(False)
		self.Bind(wx.EVT_MENU, self.generar, self.mn_generar)
		salir= menu1.Append(-1, _('&Salir'))
		self.Bind(wx.EVT_MENU, self.cerrar, salir)

	# creación del menú herramientas
		menu2= wx.Menu()
		herramientas =  barrademenu.Append(menu2, _('&Herramientas'))
		self.mn_metadatos_disco = menu2.Append(-1, _('&Metadatos del álbum'))
		self.mn_metadatos_disco.Enable(False)
		self.Bind(wx.EVT_MENU, self.guardar_disco, self.mn_metadatos_disco)
		opciones = menu2.Append(-1, _('&Opciones'))
		self.Bind(wx.EVT_MENU, self.abrir_opciones, opciones)

	#creación del menú ayuda
		menu3= wx.Menu()
		ayuda= barrademenu.Append(menu3, _('A&yuda'))
		self.documentacion = menu3.Append(-1, _('&Documentación'))
		self.Bind(wx.EVT_MENU, self.abrir_documentacion, self.documentacion)
		self.mn_buscar_actualizacion = menu3.Append(-1, _('&Buscar  actualizaciones'))
		self.Bind(wx.EVT_MENU, self.buscar_actualizacion, self.mn_buscar_actualizacion)
		acercade= menu3.Append(-1, _('Acerca de...'))
		self.Bind(wx.EVT_MENU, self.mg_acerca, acercade)


#panel y controles

		self.panel1 = wx.Panel(self)
		self.panel2= wx.Panel(self.panel1)
		self.panel2.Enable(False)
		self.l_abrir= wx.StaticText (self.panel1, -1, _('Carga el archivo de audio que quieres procesar.'))
		self.bt_abrir= wx.Button(self.panel1, -1, _('&Cargar audio'))
		self.bt_abrir.SetFocus()
		self.Bind(wx.EVT_BUTTON, self.abrir_archivo, self.bt_abrir)
		backend= wx.media.MEDIABACKEND_DIRECTSHOW
		self.reproductor= wx.media.MediaCtrl()
		self.reproductor.Create(self.panel2, style=wx.SIMPLE_BORDER, szBackend=backend)
		self.reproductor.Show(False)



		self.l_encabezado = wx.StaticText(self.panel2, -1, _('Nuevo proyecto'))
		self.font_encabezado =self.l_encabezado.GetFont()
		self.font_encabezado.SetPointSize(30)
		self.l_encabezado.SetFont(self.font_encabezado)
		self.valores= '0:0:0:0'
		self.l_reloj= wx.StaticText(self.panel2, -1, self.valores)
		self.font_reloj= self.l_reloj.GetFont()
		self.font_reloj.SetPointSize(60)
		self.l_reloj.SetFont(self.font_reloj)
		self.l_pista= wx.StaticText(self.panel2, -1, _('Línea de tiempo'))
		self.minutaje= 1
		self.linea_tiempo= wx.Slider(self.panel2, -1, 0, 0, self.minutaje,size= (400, -1))
		self.linea_tiempo.SetLineSize(5000)
		self.linea_tiempo.SetPageSize(60000)

		self.Bind(wx.EVT_SLIDER, self.mover, self.linea_tiempo)		
		self.bt_reproducir= wx.Button(self.panel2, -1, _('&Reproducir'))
		self.Bind(wx.EVT_BUTTON, self.reproducir_pausar, self.bt_reproducir)
		self.Bind(wx.media.EVT_MEDIA_STOP, self.detener, self.reproductor)
		self.timer= wx.Timer(self)
		self.timer.Start(self.reproductor.Length())
		self.Bind(wx.EVT_TIMER, self.temporizar)

		self.bt_enfocar_linea_tiempo = wx.Button(self.panel2, self.id_bt_enfocar_linea_tiempo, _('línea de tiempo'))
		self.bt_enfocar_linea_tiempo.Show(False)
		self.Bind(wx.EVT_BUTTON, self.enfocar_linea_tiempo, self.id_bt_enfocar_linea_tiempo)
		self.atajo_enfocar_linea_tiempo = wx.AcceleratorEntry(wx.ACCEL_CTRL, ord ('l'), self.id_bt_enfocar_linea_tiempo)
		self.bt_enfocar_lista = wx.Button(self.panel2, self.id_bt_enfocar_lista, _('enfocar lista'))
		self.bt_enfocar_lista.Show(False)
		self.Bind(wx.EVT_BUTTON, self.enfocar_lista, self.id_bt_enfocar_lista)
		self.atajo_enfocar_lista = wx.AcceleratorEntry(wx.ACCEL_CTRL, ord ('m'), self.id_bt_enfocar_lista)
		self.bt_duracion= wx.Button(self.panel2, self.id_hablar_duracion, _('Duración'))
		self.bt_duracion.Show(False)
		self.Bind(wx.EVT_BUTTON, self.hablar_duracion, self.id_hablar_duracion)
		self.atajo_duracion= wx.AcceleratorEntry(wx.ACCEL_CTRL, ord ('d'), self.id_hablar_duracion)
		self.bt_tiempo_actual= wx.Button(self.panel2, self.id_bt_tiempo_actual, _('tiempo actual'))
		self.bt_tiempo_actual.Show(False)
		self.Bind(wx.EVT_BUTTON, self.hablar_tiempo, self.id_bt_tiempo_actual)
		bt_detener= wx.Button(self.panel2, -1, _('&Detener'))
		self.Bind(wx.EVT_BUTTON, self.detener, bt_detener)
		l_volumen= wx.StaticText(self.panel2, -1, _('Volumen'))
		self.volumen= wx.Slider(self.panel2, -1, 100, 0, 100)
		self.Bind(wx.EVT_SLIDER, self.volumenear,self.volumen)
		self.bt_marcar= wx.Button(self.panel2, -1, _('&Marcar'))
		self.Bind(wx.EVT_BUTTON, self.marcar, self.bt_marcar)
		self.atajo_tiempo_actual= wx.AcceleratorEntry(wx.ACCEL_CTRL, ord ('t'), self.id_bt_tiempo_actual)
		self.entradas_atajos= [self.atajo_enfocar_lista, self.atajo_enfocar_linea_tiempo, self.atajo_tiempo_actual, self.atajo_duracion]
		self.tabla_atajos= wx.AcceleratorTable(self.entradas_atajos)
		self.SetAcceleratorTable(self.tabla_atajos)

		self.Bind(wx.EVT_CLOSE, self.cerrar)
# Construcción de lista
		self.l_lista = wx.StaticText(self.panel2, -1, _('Marcas'))
		self.lista= wx.ListCtrl(self.panel2, -1,style= wx.LC_REPORT|wx.LC_VRULES)
		self.lista.InsertColumn(0, 'N°')
		self.lista.InsertColumn(1, _('Título'))
		self.lista.InsertColumn(2, _('Autor'))
		self.lista.InsertColumn(3, _('Tiempo de inicio'))
		self.Bind(wx.EVT_LIST_KEY_DOWN, self.detectar_tecla_lista, self.lista)
		self.Bind(wx.EVT_LIST_ITEM_RIGHT_CLICK, self.desplegar_contextual, self.lista)
		self.Bind(wx.EVT_LIST_ITEM_FOCUSED, self.posicionar_marca, self.lista)
#		self.Bind(wx.EVT_LIST_ITEM_SELECTED, self.seleccionar_multiple, self.lista)
		self.bt_editar = wx.Button(self.panel2, -1, _('&Editar'))
		self.Bind(wx.EVT_BUTTON, self.abrir_editar2, self.bt_editar)
		self.bt_generar= wx.Button(self.panel2, -1, _('&GENERAR CUE'))
		self.bt_generar.Enable(False)
		self.Bind(wx.EVT_BUTTON, self.generar, self.bt_generar)
		self.Bind(wx.EVT_KEY_DOWN, self.detectar_tecla_principal)


#creación de sizers

		sz0 = wx.BoxSizer(wx.VERTICAL)
		sz0.Add(self.l_abrir)
		sz0.Add(self.bt_abrir)
		sz0.Add(self.panel2,  wx.SizerFlags().Expand())
		self.panel1.SetSizer(sz0)


		sz1= wx.BoxSizer(wx.VERTICAL)

		sz1.Add(self.l_encabezado, wx.SizerFlags().Center())
		sz1.Add(self.l_reloj, wx.SizerFlags().Center())
		sz1.Add(self.reproductor)

		sz1.Add(self.linea_tiempo, wx.SizerFlags().Expand())


		sz2= wx.BoxSizer(wx.HORIZONTAL)
		sz1.Add(sz2)
		sz2.Add(self.bt_reproducir)
		sz2.Add(bt_detener)
		sz2.Add(self.volumen)
		sz2.Add(self.bt_marcar)

		sz3 = wx.BoxSizer(wx.HORIZONTAL)
		sz1.Add(sz3, wx.SizerFlags().Center())
		sz3.Add(self.lista, wx.SizerFlags().Expand())

		sz4 = wx.BoxSizer(wx.VERTICAL)
		sz3.Add(sz4)
		sz4.Add(self.bt_editar)
		sz4.Add(self.bt_generar)

		self.panel2.SetSizer (sz1)

		#llamado a funciones
		self.buscar_actualizacion(None)


	# carga marcas en  la lista
	def listar(self):
		id = self.lista.GetItemCount()
		for marca in self.controlador.getMarcas():
			self.lista.InsertStringItem(id, str(marca.id))
			self.lista.SetStringItem(id, 1,  marca.titulo)
			self.lista.SetStringItem(id, 2, marca.autor)
			self.lista.SetStringItem(id, 3,marca.tiempo_inicio)
			id+=1



	def refrescar_principal(self):
		self.graficar()
		self.refrescar_lista()

	def refrescar_lista(self):
		self.lista.DeleteAllItems()
		self.listar()


	def detectar_tecla_lista(self, event):
		tecla = event.GetKeyCode()
		if tecla == wx.WXK_DELETE:
			self.borrar_item(None)
		elif tecla == wx.WXK_WINDOWS_MENU:
			self.desplegar_contextual(event)

	def detectar_tecla_principal(self, event):
		tecla = event.GetKeyCode()
		if tecla == wx.WXK_F1:
			self.abrir_documentacion(None)

	def posicionar_marca(self, event):
		''' Posiciona el inicio de reproducción según el tiempo de inicio de cada marca '''
		item = self.lista.GetFocusedItem()
		marca =self.controlador.getMarcas()[item]
		self.reproductor.Seek(marca.milesimas)

	def borrar_item(self, event):
		''' Elimina las marcas seleccionadas en la lista '''
		item = self.lista.GetFocusedItem()
		cantidad = self.lista.GetItemCount()
		for marca in reversed(range(cantidad)):
			sl = self.lista.IsSelected(marca)
			if sl == True:
				self.controlador.borrar_marca(marca)
		self.refrescar_lista()
		if cantidad != 0:
			self.lector.output(_('Eliminado'))

	def desplegar_contextual(self, event):
		''' Despliega el menú contextual de la lista de marcas '''
		self.PopupMenu(Contextual(self))

	def cerrar (self, event):
		if os.path.exists('temp.proyecto.cgp'):
			resp = wx.MessageBox(_('Estás a punto de cerrar el programa. Los cambios que hayas echo al proyecto no se guardarán. \n ¿Deseas salir?'), _('Advertencia.'), style= wx.YES_NO|wx.NO_DEFAULT| wx.ICON_WARNING)
			if resp == wx.YES:
				self.controlador.limpiar_temporal()
				self.Destroy()
		else:
			self.Destroy()

	def guardar_disco(self, event):
		self.vn_disco = vista.disco.Disco(self, _('Metadatos del álbum'), self.controlador)
		if self.vn_disco.ShowModal() == wx.ID_OK:
			self.controlador.crear_disco(self.vn_disco.getTitulo(),
			self.vn_disco.getAutor(),
			self.vn_disco.getFecha(),
			self.vn_disco.getGenero(),
			self.vn_disco.getComentarios())
			self.mn_metadatos_disco.Enable(True)
			self.l_encabezado.SetLabel(self.controlador.consultar_disco().titulo + ' - ' + self.controlador.consultar_disco(). autor)



	def abrir_archivo (self, event):
		self.dialogo= wx.FileDialog(self, _('Cargar audio'), style=wx.FD_OPEN)
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
				wx.MessageBox(_('No es posible cargar el fichero, sólo se admiten archivos de audio.'), caption= 'Atención.', style= wx.ICON_ERROR)
			else:
				self.reproductor.Load(self.path)
				self.controlador.crear_proyecto()
				self.guardar_disco(None)
				self.registrar_pista()
				self.habilitar_controles()
				self.desactivar_controles()
				self.linea_tiempo.SetFocus()


	def registrar_pista(self):
		direccion = os.path.dirname(self.path)
		nombre_completo = os.path.basename(self.path)
		nombre = os.path.splitext(nombre_completo)[0]
		self.controlador.crear_pista(
		nombre,
		os.path.splitext(nombre_completo)[1],
		direccion,
		self.reproductor.Length())

	def habilitar_controles (self):
		if self.controlador.pista != None:
			self.panel2.Enable(True)
			self.mn_metadatos_disco.Enable(True)
			self.mn_nuevo_proyecto.Enable(True)
		if self.controlador.data != None:
			self.mn_generar.Enable(True)
			self.mn_guardar_proyecto.Enable(True)
			self.bt_generar.Enable(True)

	# desactiva controles
	def desactivar_controles(self):
		if self.controlador.pista != None:
			self.bt_abrir.Enable(False)
			self.mn_cargar_audio.Enable(False)

	#abre un proyecto existente
	def abrir_proyecto(self, event):
		self.dialogo_abrir_proyecto = wx.FileDialog(self, _('Abrir proyecto'), style=wx.FD_OPEN, wildcard= '*.CGP')
		if self.dialogo_abrir_proyecto.ShowModal() == wx.ID_OK:
			if self.controlador.ruta_proyecto != self.dialogo_abrir_proyecto.GetPath():
				mensaje = wx.MessageBox(_('Estás a punto de abrir un nuevo proyecto. Los cambios que hayas hecho se perderán. \n ¿Deseas continuar de todos modos?'), _('Advertencia.'), style= wx.YES_NO| wx.NO_DEFAULT| wx.ICON_WARNING)
				if mensaje == 2:
					self.controlador.limpiar_temporal()
					self.controlador.ruta_proyecto = self.dialogo_abrir_proyecto.GetPath()
					self.controlador.crear_proyecto()
					self.controlador.load()
					self.refrescar_lista()
					self.habilitar_controles()
					self.desactivar_controles()

	# Crea un nuevo proyecto
	def crear_proyecto(self, event):
		mensaje = wx.MessageBox(_('Estás a punto de crear un nuevo proyecto. Los cambios que hayas hecho se perderán. \n ¿Deseas continuar de todos modos?'), _('Advertencia.'), style= wx.YES_NO| wx.NO_DEFAULT| wx.ICON_WARNING)
		if mensaje == 2:
			self.controlador.limpiar_temporal()
			self.controlador.load()
			self.path = ''
			self.controlador.crear_proyecto()
			self.habilitar_controles()
			self.refrescar_principal()

	#guarda el proyecto en una ruta específica
	def guardar_proyecto(self, event):
		self.dialogo_guardar = wx.FileDialog(self, _('Guardar proyecto'), style=wx.FD_SAVE, wildcard= '*.CGP')
		if self.dialogo_guardar.ShowModal() == wx.ID_OK:
			self.controlador.ruta_proyecto = self.dialogo_guardar.GetPath()
			self.controlador.save()
			self.controlador.limpiar_temporal()

	#abre la ventana de opciones
	def abrir_opciones(self, event):
		vn_opciones = vista.opciones.Opciones(self, _('Opciones'))
		if vn_opciones.ShowModal() == wx.ID_OK:
			vn_opciones.guardar_opciones()
			self.refrescar_principal()

	def abrir_documentacion(self, event):
		if self.controlador_opciones.consultar_opciones('str', 'general', 'idioma') == 'es':
			os.startfile(os.path.join('files', 'documentation', 'es.html'))
		else:
			os.startfile(os.path.join('files', 'documentation', 'en.html'))

	#busca actualizaciones
	def buscar_actualizacion(self, event):
		self.controlador_app.verificarNuevaVersion()
		if self.controlador_app.actualizado == False:
			if self.controlador_opciones.consultar_opciones('bool', 'general', 'sonido_actualizacion'):
				wx.adv.Sound.PlaySound(os.path.join('files', 'sounds', 'nueva_version.wav'))
			res =wx.MessageBox(_('Hay una nueva versión disponible. ¿Deseas descargarla ahora?'), style= wx.YES_NO)
			if res == wx.YES:
				self.controlador_app.descargar_version()
		elif self.controlador_app.actualizado == True and event != None:
			wx.MessageBox(_('No hay ninguna nueva versión disponible'), _('Aviso.'))

# muestra información acerca del programa
	def mg_acerca(self, event):
		dlg = Acerca_de(self, title= _('Acerca de...'))
		if dlg.ShowModal() == wx.ID_OK:
			dlg.close()

	def enfocar_linea_tiempo(self, event):
		self.linea_tiempo.SetFocus()

	def enfocar_lista(self, event):
		self.lista.SetFocus()

# reproduce o pausa la pista.
	def reproducir_pausar (self, event):
		self.estado= self.reproductor.GetState()
		if self.estado == 1 or self.estado == 0:
			self.reproductor.Play()
			self.bt_reproducir.SetLabel(_('&Pausar'))
			self.minutaje= self.reproductor.Length()
			self.linea_tiempo.SetMax(self.minutaje)
		elif self.estado == 2:
			self.reproductor.Pause()
			self.bt_reproducir.SetLabel(_('&Reproducir'))

#pausa la reproducción
	def pausar(self, event):
		self.estado= self.reproductor.GetState()
		if self.estado == 2:
			self.reproductor.Pause()
			self.bt_reproducir.SetLabel(_('&Reproducir'))

# detiene la reproducción
	def detener (self, event):
		self.estado= self.reproductor.GetState()
		if self.estado == 1 or self.estado == 2:
			self.reproductor.Stop()
			self.bt_reproducir.SetLabel(_('&Reproducir'))
			self.editar.reproduciendo = False
			self.editar.cambiar_etiqueta()
		else:
			self.bt_reproducir.SetLabel(_('&Reproducir'))
			self.editar.reproduciendo = False
			self.editar.cambiar_etiqueta()

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
		self.reproductor.Seek(self.linea_tiempo.GetValue())

#mueve la aguja del control de la pista de forma automática a medida que se reproduce el audio
	def temporizar (self, event):
		self.tiempo= self.reproductor.Tell()
		self.linea_tiempo.SetValue(self.tiempo)
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
		if self.controlador.pista != None:
			self.controlador.pista.reproducción_actual = self.tiempo

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
		self.lector.output(str(self.horas) + _('horas') + str(self.minutos) + _('minutos') + str(self.segundos) + _('segundos') + str(self.marcos) + _('marcos'))

# verbaliza el tiempo de duración del archivo de audio.
	def hablar_duracion (self, event):
		self.duracion= self.reproductor.Length()
		valores= self.calcular_tiempo(self.duracion)
		self.lector.output(_('Duración de la pista. ') + str(valores[0]) + _('horas') + str(valores [1]) + _('minutos') + str(valores [2]) + _('segundos') + str(valores [3]) + _('marcos'))

	def marcar (self, event):
		self.reproductor.Pause()
		self.bt_reproducir.SetLabel(_('&Reproducir'))
		if self.controlador_opciones.consultar_opciones('bool', 'general', 'sonido_marca'): 
			wx.adv.Sound.PlaySound( os.path.join('files', 'sounds', 'marca.wav'))
		self.vn_editar()


	def vn_editar(self):
		self.editar = Editar(self, _('Crear marca'), self.controlador)
		self.editar.getTiempo(self.reproductor.Tell())
#		self.editar.tiempo_actual = self.reproductor.Tell()
		self.editar.Bind(wx.EVT_BUTTON, self.reproducir_editar, self.editar.bt_reproducir)
		self.editar.duracion_tiempo = self.calcular_tiempo(self.reproductor.Length())
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
			self.habilitar_controles()
		else:
			self.pausar(None)
#			self.bt_generar.Enable(True)
#			self.mn_generar.Enable(True)
#			self.mn_guardar_proyecto.Enable(True)

	def abrir_editar2(self,event):
		self.editar2 = Editar2(self, _('Editar marca'), self.controlador)
		item = self.lista.GetFocusedItem()
		self.editar2.id = item
		if self.editar2.ShowModal() == wx.ID_OK:
			pass

	def generar(self, event):
		self.controlador.generar_cue(self.controlador_opciones.consultar_opciones('bool', 'general', 'cue_id'))
		existe = self.controlador.verificar_exportacion()
		if existe == True:
			if self.controlador_opciones.consultar_opciones('bool', 'general', 'sonido_generar'):
				wx.adv.Sound.PlaySound( os.path.join('files', 'sounds', 'ok.wav'))
			msg = wx.adv.NotificationMessage('', _('Cue generado exitosamente.'), self, wx.ICON_INFORMATION)
			msg.Show(5)


class Contextual(wx.Menu):
	def __init__(self, parent):
		super(Contextual, self).__init__()
		self.parent = parent
		self.m1 = wx.MenuItem(self, wx.NewId(), _('&Editar'))
		self.AppendItem(self.m1)
		self.Bind(wx.EVT_MENU, self.abrir_editar2, self.m1)
		self.m2 = wx.MenuItem(self, -1, _('E&liminar'))
		self.AppendItem(self.m2)
		self.Bind(wx.EVT_MENU, self.borrar_item, self.m2)


	def abrir_editar2(self, event):
		self.parent.abrir_editar2(None)

	def borrar_item(self, event):
		self.parent.borrar_item(None)