import pdb
import os
import sys

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
from .informacion_medios import Informacion_medios


class Frame(wx.Frame):
	def __init__(self, parent, title, controlador, app, opciones):
		super().__init__(parent, title= title, style = wx.DEFAULT_FRAME_STYLE|wx.MAXIMIZE)
		self.syze = (800,800)
		self.controlador = controlador
		self.controlador_app = app
		self.controlador_opciones = opciones
		self.Center()
		self.alertar_instancia()
		self.graficar()
		self.Show()



	#creación de controles
	def graficar(self):
		traductor = Traductor('labrandeos')
		
		# creación de lector
		self.lector= accessible_output2.outputs.auto.Auto()

		#ID personalizados
		self.id_bt_enfocar_lista = wx.NewIdRef()
		self.id_bt_enfocar_linea_tiempo = wx.NewIdRef()
		self.id_bt_tiempo_actual= wx.NewIdRef()
		self.id_hablar_duracion= wx.NewIdRef()
		self.id_mn_deshacer = wx.NewIdRef()
		self.id_mn_nuevo_proyecto = wx.NewIdRef()
		self.id_mn_abrir_proyecto = wx.NewIdRef()
		self.id_mn_guardar = wx.NewIdRef()
		self.id_mn_rehacer = wx.NewIdRef()
		self.id_mn_metadatos_disco = wx.NewIdRef()
		self.id_mn_opciones = wx.NewIdRef()
		self.id_mn_documentacion = wx.NewIdRef()
		self.id_mn_editar_marca = wx.NewIdRef()
		self.id_mn_informacion = wx.NewIdRef()
		



# creacion de la barra de menu.
		self.barrademenu= wx.MenuBar()
		self.SetMenuBar(self.barrademenu)

	#creación del menú archivo
		menu1= wx.Menu()
		archivo = self.barrademenu.Append(menu1, _('&Archivo'))
		self.mn_nuevo_proyecto = menu1.Append(self.id_mn_nuevo_proyecto, _('&Nuevo proyecto') + '\tCtrl+n')
		self.mn_nuevo_proyecto.Enable(False)
		self.Bind(wx.EVT_MENU, self.crear_proyecto, self.mn_nuevo_proyecto)
		self.atajo_mn_nuevo_proyecto = wx.AcceleratorEntry(wx.ACCEL_CTRL, ord ('n'), self.id_mn_nuevo_proyecto)
		self.mn_cargar_audio = menu1.Append(-1, _('&Cargar audio'))
		self.Bind(wx.EVT_MENU, self.abrir_archivo, self.mn_cargar_audio)
		self.mn_abrir_proyecto = menu1.Append(self.id_mn_abrir_proyecto, _('&Abrir proyecto') + '\tCtrl+O')
		self.Bind(wx.EVT_MENU, self.abrir_proyecto, self.mn_abrir_proyecto)
		self.atajo_abrir_proyecto = wx.AcceleratorEntry(wx.ACCEL_CTRL, ord ('o'), self.id_mn_abrir_proyecto)
		self.mn_guardar = menu1.Append(self.id_mn_guardar, _('&Guardar') + '\tCtrl+S')
		self.mn_guardar.Enable(False)
		self.Bind(wx.EVT_MENU, self.guardar, self.mn_guardar)
		self.atajo_guardar = wx.AcceleratorEntry(wx.ACCEL_CTRL, ord ('s'), self.id_mn_guardar)	
		self.mn_guardar_como = menu1.Append(-1, _('G&uardar como...'))
		self.mn_guardar_como.Enable(False)
		self.Bind(wx.EVT_MENU, self.guardar_proyecto, self.mn_guardar_como)
		self.mn_exportar = menu1.Append(-1, _('&Exportar CUE'))
		self.mn_exportar.Enable(False)
		self.Bind(wx.EVT_MENU, self.exportar, self.mn_exportar)
		salir= menu1.Append(-1, _('&Salir'))
		self.Bind(wx.EVT_MENU, self.cerrar, salir)

		#creacion del menu editar
		menu2= wx.Menu()
		self.mn_editar =  self.barrademenu.Append(menu2, _('&Editar'))
		self.mn_deshacer = menu2.Append(self.id_mn_deshacer, _('&Deshacer') + '\tCtrl+Z')
		self.mn_deshacer.Enable()
		self.Bind(wx.EVT_MENU, self.deshacer, self.id_mn_deshacer)
		self.atajo_deshacer = wx.AcceleratorEntry(wx.ACCEL_CTRL, ord ('z'), self.id_mn_deshacer)
		self.mn_rehacer = menu2.Append(self.id_mn_rehacer, _('&Rehacer') + '\tCtrl+Shift+Z')
		self.Bind(wx.EVT_MENU, self.rehacer, self.id_mn_rehacer)
		self.mn_rehacer.Enable(False)
		self.atajo_rehacer = wx.AcceleratorEntry(wx.ACCEL_CTRL|wx.ACCEL_SHIFT, ord ('z'), self.id_mn_rehacer)
		self.mn_eliminar = menu2.Append(-1, _('&Eliminar') + '\tSupr')
		self.Bind(wx.EVT_MENU, self.borrar_item, self.mn_eliminar)
		self.mn_eliminar.Enable(False)
		self.mn_marca = menu2.Append(self.id_mn_editar_marca, _('&Marca') + '\tCtrl+e')
		self.Bind(wx.EVT_MENU, self.editar_marca, self.id_mn_editar_marca)
		self.mn_marca.Enable(False)
		self.atajo_editar_marca = wx.AcceleratorEntry(wx.ACCEL_CTRL, ord ('e'), self.id_mn_editar_marca)





		# creación del menú herramientas
		menu3= wx.Menu()
		herramientas =  self.barrademenu.Append(menu3, _('&Herramientas'))
		self.mn_metadatos_disco = menu3.Append(self.id_mn_metadatos_disco, _('&Metadatos del álbum') + '\tCtrl+Shift+M')
		self.mn_metadatos_disco.Enable(False)
		self.Bind(wx.EVT_MENU, self.guardar_disco, self.mn_metadatos_disco)
		self.atajo_metadatos_disco = wx.AcceleratorEntry(wx.ACCEL_CTRL|wx.ACCEL_SHIFT, ord ('m'), self.id_mn_metadatos_disco)
		self.mn_informacion = menu3.Append(self.id_mn_informacion, _('&Información de medios') + '\tCtrl+I')
		self.Bind(wx.EVT_MENU, self.informar_medios, self.id_mn_informacion)
		self.atajo_informacion = wx.AcceleratorEntry(wx.ACCEL_CTRL, ord ('i'), self.id_mn_informacion)
		self.mn_informacion.Enable(False)
		self.mn_opciones = menu3.Append(self.id_mn_opciones, _('&Opciones') + '\tCtrl+P')
		self.Bind(wx.EVT_MENU, self.abrir_opciones, self.mn_opciones)
		self.atajo_opciones = wx.AcceleratorEntry(wx.ACCEL_CTRL, ord ('p'), self.id_mn_opciones)

	#creación del menú ayuda
		menu4= wx.Menu()
		ayuda= self.barrademenu.Append(menu4, _('A&yuda'))
		self.mn_documentacion = menu4.Append(self.id_mn_documentacion, _('&Documentación') + '\tF1')
		self.Bind(wx.EVT_MENU, self.abrir_documentacion, self.mn_documentacion)
		self.atajo_documentacion = wx.AcceleratorEntry(wx.ACCEL_NORMAL, wx.WXK_F1, self.id_mn_documentacion) 
		self.mn_buscar_actualizacion = menu4.Append(-1, _('&Buscar actualizaciones'))
		self.Bind(wx.EVT_MENU, self.buscar_actualizacion, self.mn_buscar_actualizacion)
		acercade= menu4.Append(-1, _('Acerca de ') + self.controlador_app.nombre_app)
		self.Bind(wx.EVT_MENU, self.mg_acerca, acercade)


#panel y controles

		self.panel1 = wx.Panel(self)
		self.panel2= wx.Panel(self.panel1)
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
		self.linea_tiempo= wx.Slider(self.panel2, -1, self.controlador.reproductor.tiempo_actual, 0, self.minutaje,size= (400, -1))
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
		self.volumen= wx.Slider(self.panel2, -1, self.controlador.reproductor.volumen * 100, 0, 100)
		self.Bind(wx.EVT_SLIDER, self.volumenear,self.volumen)
		self.bt_marcar= wx.Button(self.panel2, -1, _('&Marcar'))
		self.bt_marcar.Enable(False)
		self.Bind(wx.EVT_BUTTON, self.marcar, self.bt_marcar)
		self.atajo_tiempo_actual= wx.AcceleratorEntry(wx.ACCEL_CTRL, ord ('t'), self.id_bt_tiempo_actual)
		self.entradas_atajos= [self.atajo_enfocar_lista, self.atajo_enfocar_linea_tiempo, self.atajo_tiempo_actual, self.atajo_duracion, self.atajo_guardar, self.atajo_deshacer, self.atajo_rehacer, self.atajo_mn_nuevo_proyecto, self.atajo_abrir_proyecto, self.atajo_metadatos_disco, self.atajo_opciones, self.atajo_documentacion, self.atajo_editar_marca, self.atajo_informacion]
		self.tabla_atajos= wx.AcceleratorTable(self.entradas_atajos)
		self.SetAcceleratorTable(self.tabla_atajos)

		self.Bind(wx.EVT_CLOSE, self.cerrar)
# Construcción de lista
		self.l_lista = wx.StaticText(self.panel2, -1, _('Marcas'))
		self.lista= wx.ListCtrl(self.panel2, -1,style= wx.LC_REPORT|wx.LC_VRULES|wx.LC_SINGLE_SEL)
		self.lista.InsertColumn(0, 'N°')
		self.lista.InsertColumn(1, _('Título'))
		self.lista.InsertColumn(2, _('Autor'))
		self.lista.InsertColumn(3, _('Tiempo de inicio'))
		self.Bind(wx.EVT_LIST_KEY_DOWN, self.detectar_tecla_lista, self.lista)
		self.Bind(wx.EVT_LIST_ITEM_RIGHT_CLICK, self.desplegar_contextual, self.lista)
		self.Bind(wx.EVT_LIST_ITEM_FOCUSED, self.posicionar_marca, self.lista)
#		self.Bind(wx.EVT_LIST_ITEM_SELECTED, self.seleccionar_multiple, self.lista)
		self.bt_exportar= wx.Button(self.panel2, -1, _('E&XPORTAR CUE'))
		self.bt_exportar.Enable(False)
		self.Bind(wx.EVT_BUTTON, self.exportar, self.bt_exportar)


# creación de sizers

		self.sz0 = wx.BoxSizer(wx.VERTICAL)
		self.sz0.Add(self.l_abrir)
		self.sz0.Add(self.bt_abrir)
		self.sz0.Add(self.panel2,  wx.SizerFlags().Expand())
		self.panel1.SetSizer(self.sz0)


		self.sz1= wx.BoxSizer(wx.VERTICAL)

		self.sz1.Add(self.l_encabezado, wx.SizerFlags().Center())
		self.sz1.Add(self.l_reloj, wx.SizerFlags().Center())
		self.sz1.Add(self.reproductor)

		self.sz1.Add(self.linea_tiempo, wx.SizerFlags().Expand())


		self.sz2= wx.BoxSizer(wx.HORIZONTAL)
		self.sz1.Add(self.sz2)
		self.sz2.Add(self.bt_reproducir)
		self.sz2.Add(bt_detener)
		self.sz2.Add(self.volumen)
		self.sz2.Add(self.bt_marcar)

		self.sz3 = wx.BoxSizer(wx.HORIZONTAL)
		self.sz1.Add(self.sz3, flag= wx.ALL|wx.CENTER) 
		self.sz3.Add(self.lista,flag= wx.ALL|wx.CENTER)

		self.sz4 = wx.BoxSizer(wx.VERTICAL)
		self.sz3.Add(self.sz4)
		self.sz4.Add(self.bt_exportar)


		self.panel2.SetSizer (self.sz1)
		self.panel2.Enable(False)

		#llamado a funciones
		self.buscar_actualizacion(None)


	# carga marcas en  la lista
	def listar(self):
		id = self.lista.GetItemCount()
		for marca in self.controlador.getMarcas():
			self.lista.InsertItem(id, str(marca.id))
			self.lista.SetItem(id, 1,  marca.titulo)
			self.lista.SetItem(id, 2, marca.autor)
			self.lista.SetItem(id, 3,marca.tiempo_inicio)
			id+=1



	def refrescar_principal(self):
#		self.refrescar_lista()
		self.panel1.Destroy()
		self.graficar()
		self.Show()
		self.Layout()
		if self.controlador.pista != None:
			self.reproductor.Load(self.controlador.pista.ruta)
		self.habilitar_controles()
		self.desactivar_controles()


	def refrescar_lista(self):
		self.lista.DeleteAllItems()
		self.listar()


	def detectar_tecla_lista(self, event):
		tecla = event.GetKeyCode()
		if tecla == wx.WXK_DELETE:
			self.borrar_item(None)
		elif tecla == wx.WXK_WINDOWS_MENU:
			self.desplegar_contextual(event)

	def posicionar_marca(self, event):
		''' Posiciona el inicio de reproducción según el tiempo de inicio de cada marca '''
		item = self.lista.GetFocusedItem()
		self.controlador.reproductor.marca_id = item
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
		self.controlador_opciones.guardar_opciones('general', 'idioma', str(self.controlador_opciones.modelo_configuracion.idioma_app))
		if self.controlador.pista != None:
			self.detectar_cambios()
			self.controlador.limpiar_temporal()
			self.Destroy()
		else:
			self.controlador.limpiar_temporal()
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
			self.mn_deshacer.Enable(True)
			self.vn_disco.guardar_datos()
			self.cambiar_encabezado()
		else:
			self.cambiar_encabezado()

	def cambiar_encabezado(self):
		if self.controlador.data.titulo != '' and self.controlador.data.autor == '':
			self.l_encabezado.SetLabel(self.controlador.data.titulo + ' - ' + _('Sin autor'))
		elif self.controlador.data.titulo == '' and self.controlador.data.autor != '':
			self.l_encabezado.SetLabel(_('Sin título') + ' - ' + self.controlador.data.autor)
		elif self.controlador.data.titulo != '' and self.controlador.data.autor != '':
			self.l_encabezado.SetLabel(self.controlador.data.titulo + ' - ' + self.controlador.data.autor)
		else:
			self.l_encabezado.SetLabel(_('Sin título') + ' - ' + _('Sin autor'))



	def abrir_archivo (self, event):
		self.dialogo= wx.FileDialog(self, _('Cargar audio'), style=wx.FD_OPEN)
		if self.dialogo.ShowModal() == wx.ID_OK:
			self.path = self.dialogo.GetPath()
			tipo_archivo = self.controlador.comprobar_medios(self.path)
			if tipo_archivo == None or tipo_archivo[0] != 'audio':
				wx.MessageBox(_('No es posible cargar el fichero, sólo se admiten archivos de audio.'), caption= 'Atención', style= wx.ICON_ERROR)
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
		self.path,
		self.reproductor.Length())

	def habilitar_controles (self):
		if self.controlador.pista != None:
			self.panel2.Enable(True)
			self.mn_metadatos_disco.Enable(True)
			self.mn_informacion.Enable(True)
			self.mn_nuevo_proyecto.Enable(True)
			self.mn_deshacer.Enable(True)
			self.bt_marcar.Enable(True)
		if self.controlador.data != None:
			self.mn_exportar.Enable(True)
			self.mn_guardar.Enable(True)
			self.mn_guardar_como.Enable(True)
			self.bt_exportar.Enable(True)
		if self.controlador.data.lista_marcas != []:
			self.mn_eliminar.Enable(True)
			self.mn_marca.Enable(True)

	# desactiva controles
	def desactivar_controles(self):
		if self.controlador.pista != None:
			self.bt_abrir.Enable(False)
			self.mn_cargar_audio.Enable(False)

	#abre un proyecto existente
	def abrir_proyecto(self, event):
		self.dialogo_abrir_proyecto = wx.FileDialog(self, _('Abrir proyecto'), style=wx.FD_OPEN, wildcard= '*.lap')
		if self.dialogo_abrir_proyecto.ShowModal() == wx.ID_OK:
			mensaje = 0
			if self.controlador.pista != None:
				mensaje = wx.MessageBox(_('Estás a punto de abrir un nuevo proyecto. Los cambios que hayas hecho se perderán. \n ¿Deseas continuar?'), _('Atención'), style= wx.OK|wx.CANCEL| wx.CANCEL_DEFAULT| wx.ICON_EXCLAMATION)
			if self.controlador.pista == None or mensaje == 2:
				self.controlador.limpiar_temporal()
				self.controlador.ruta_proyecto = self.dialogo_abrir_proyecto.GetPath()
				self.controlador.crear_proyecto()
				self.controlador.load()
				self.reproductor.Load(self.controlador.pista.ruta)
				self.refrescar_lista()
				self.l_encabezado.SetLabel(self.controlador.disco.titulo + ' - ' + self.controlador.disco.autor)
				self.habilitar_controles()
				self.desactivar_controles()

	def detectar_cambios(self):
		''' Detecta si se han hecho cambios en el proyecto actual para que sean guardados '''
		if self.controlador.comparar_modelo() != True:
			mensaje = wx.MessageBox(_('¿Deseas guardar los cambios realizados?'), _('Guardar'), style= wx.YES_NO|wx.CANCEL|wx.YES_DEFAULT| wx.ICON_QUESTION)
			if mensaje == wx.YES and self.controlador.es_temporal() == True:
				self.guardar_proyecto(None)
			elif mensaje == wx.YES and self.controlador.es_temporal() == False:
				self.guardar(None)
			elif mensaje == wx.CANCEL:
				raise Exception('Cancelado')

	def crear_proyecto(self, event):
		''' Crea un nuevo proyecto '''
		self.detectar_cambios()
		self.controlador.limpiar_temporal()
		self.controlador.load()
		self.path = ''
		self.controlador.limpiar_proyecto()
		self.controlador.crear_proyecto()
		self.controlador.save()
		self.habilitar_controles()
		self.refrescar_principal()
		self.lector.output(_('Nuevo proyecto'))


	#guardar cambios en proyecto actual
	def guardar(self, event):
		self.controlador.save()
		self.lector.output(_('guardado'))

	#guarda el proyecto en una ruta específica
	def guardar_proyecto(self, event):
		self.dialogo_guardar = wx.FileDialog(self, _('Guardar proyecto'), style=wx.FD_SAVE, wildcard= '*.lap')
		if self.dialogo_guardar.ShowModal() == wx.ID_OK:
			if os.path.isfile(self.dialogo_guardar.GetPath()):
				mensaje = wx.MessageBox(_('Ya existe un fichero con este nombre. ¿Deseas reemplazarlo?'), _('Atención'), style= wx.YES_NO|wx.NO_DEFAULT| wx.ICON_EXCLAMATION)
				if mensaje == 2:
					self.controlador.ruta_proyecto = self.dialogo_guardar.GetPath()
					self.controlador.save()
					self.controlador.limpiar_temporal()
			else:
				self.controlador.ruta_proyecto = self.dialogo_guardar.GetPath()
				self.controlador.save()
				self.controlador.limpiar_temporal()
		else:
			raise Exception('Cancelado')

	#abre la ventana de opciones
	def abrir_opciones(self, event):
		self.vn_opciones = vista.opciones.Opciones(self, _('Opciones'), opciones= self.controlador_opciones)
		idioma_anterior = self.vn_opciones.com_idioma.GetValue()
		if self.vn_opciones.ShowModal() == wx.ID_OK:
			self.vn_opciones.guardar_opciones()
			idioma_posterior = self.vn_opciones.com_idioma.GetValue()
			if idioma_anterior != idioma_posterior:
				wx.MessageBox(_('Debes reiniciar el programa para que los cambios de idioma surtan efecto.'), _('Atención'), style= wx.ICON_EXCLAMATION)

	def abrir_documentacion(self, event):
		if self.controlador_opciones.consultar_opciones('str', 'general', 'idioma') == 'es':
			os.startfile(os.path.join('files', 'documentation', 'es.html'))
		else:
			os.startfile(os.path.join('files', 'documentation', 'en.html'))

	def alertar_instancia(self):
		''' Muestra alerta si se abre una nueva instancia del programa ''' 
		if self.controlador_app.verificar_instancia():
			wx.MessageBox(self.controlador_app.nombre_app + _(' ya se está ejecutando.'), _('Aviso'), style= wx.ICON_INFORMATION)
			sys.exit(1)

	def buscar_actualizacion(self, event):
		''' Muestra mensajes si hay o no actualizaciones '''
		self.controlador_app.verificarNuevaVersion()
		if self.controlador_app.actualizado == False:
			if self.controlador_opciones.consultar_opciones('bool', 'general', 'sonido_actualizacion'):
				wx.adv.Sound.PlaySound(os.path.join('files', 'sounds', 'nueva_version.wav'))
			res =wx.MessageBox(_('Hay una nueva versión disponible. ¿Deseas descargarla ahora?'), _('Actualización'), style= wx.YES_NO|wx.ICON_ASTERISK)
			if res == wx.YES:
				self.controlador_app.descargar_version()
		elif self.controlador_app.actualizado == True and event != None:
			wx.MessageBox(_('No hay ninguna nueva versión disponible'), _('Aviso'), style= wx.ICON_INFORMATION)

# muestra información acerca del programa
	def mg_acerca(self, event):
		dlg = Acerca_de(self, title= _('Acerca de ') + self.controlador_app.nombre_app)
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
		else:
			self.bt_reproducir.SetLabel(_('&Reproducir'))

	# controla el volumen
	def volumenear (self, event):
		a= self.volumen.GetValue()
		b= a /100
		self.reproductor.SetVolume(b)
		self.controlador.reproductor.volumen = b

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
			self.controlador.reproductor.tiempo_actual = self.tiempo

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
		self.editar = Editar(self, _('Crear marca'), self.controlador, self.reproductor)
		self.editar.getTiempo(self.reproductor.Tell())
		self.editar.tiempo_actual = self.reproductor.Tell()
		self.editar.duracion_tiempo = self.calcular_tiempo(self.reproductor.Length())
		if self.editar.ShowModal() == wx.ID_OK:
			self.pausar(None)
			marca = self.controlador.crearMarca(self.lista.GetItemCount(),
				self.editar.getTitulo(),
				self.editar.getAutor(),
				self.editar.getTiempoInicio(),
				self.editar.tiempo_actual)
			id=self.lista.GetItemCount()
			self.lista.InsertItem(id,  str(marca.id))
			self.lista.SetItem(id, 1, marca.titulo)
			self.lista.SetItem(id, 2, marca.autor)
			self.lista.SetItem(id, 3, marca.tiempo_inicio)
			self.refrescar_lista()
			self.habilitar_controles()
		else:
			self.pausar(None)

	def editar_marca(self,event):
		self.editar2 = Editar2(self, _('Editar marca'), self.controlador, self.reproductor)
		self.pausar(None)
		item = self.lista.GetFocusedItem()
		marca = self.controlador.consultar_datos(item)
		self.editar2.getTiempo(marca.milesimas)
		if self.editar2.ShowModal() == wx.ID_OK:
			self.pausar(None)
			marca = self.controlador.editarMarca(item,
				self.editar2.getTitulo(),
				self.editar2.getAutor(),
				self.editar2.getTiempoInicio(),
				self.editar2.tiempo_actual)
			self.lista.SetItem(item, 0,   str(marca.id))
			self.lista.SetItem(item, 1, marca.titulo)
			self.lista.SetItem(item, 2, marca.autor)
			self.lista.SetItem(item, 3, marca.tiempo_inicio)
			self.refrescar_lista()
			self.habilitar_controles()
		else:
			self.pausar(None)

	def exportar(self, event):
		self.controlador.exportar_cue(self.controlador_opciones.consultar_opciones('bool', 'general', 'cue_id'))
		if self.controlador_opciones.consultar_opciones('bool', 'general', 'sonido_exportar'):
			wx.adv.Sound.PlaySound( os.path.join('files', 'sounds', 'ok.wav'))
		msg = wx.adv.NotificationMessage('', _('Cue generado exitosamente.'), self, wx.ICON_INFORMATION)
		msg.Show(5)
		if self.controlador_opciones.consultar_opciones('bool', 'general', 'ABRIR_CARPETA'):
			wx.LaunchDefaultBrowser(self.controlador.pista.direccion)

	def deshacer(self, event):
		self.controlador.deshacer()
		self.lector.output(_('Deshacer'))
		self.mn_rehacer.Enable(True)
		self.refrescar_lista()
		if self.controlador.historial.es_vacia()[0]:
			self.mn_deshacer.Enable(False)


	def rehacer(self, event):
		if self.controlador.historial.es_vacia()[1] == False: 
			self.controlador.rehacer()
			self.refrescar_lista()
			self.lector.output(_('Rehacer'))
		if self.controlador.historial.es_vacia()[1] == True:
			self.mn_rehacer.Enable(False)

	def informar_medios(self, event):
		self.vn_informacion = Informacion_medios(None, _('Información de medios'), self.controlador)
		if self.vn_informacion.ShowModal() == wx.OK:
			self.vn_informacion.close()



class Contextual(wx.Menu):
	def __init__(self, parent):
		super(Contextual, self).__init__()
		self.parent = parent
		self.m1 = wx.MenuItem(self, wx.NewId(), _('&Editar') +  '\tCtrl+E')
		self.Append(self.m1)
		self.Bind(wx.EVT_MENU, self.abrir_editar2, self.m1)
		self.m2 = wx.MenuItem(self, -1, _('E&liminar'))
		self.Append(self.m2)
		self.Bind(wx.EVT_MENU, self.borrar_item, self.m2)


	def abrir_editar2(self, event):
		self.parent.editar_marca(None)

	def borrar_item(self, event):
		self.parent.borrar_item(None)

