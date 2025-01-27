import logging
import os
import subprocess
import sys

import accessible_output2.outputs.auto
import wx.media
import wx
import wx.adv

from controlador.traductor import Traductor

import vista.disco
import vista.opciones
from .editar import Editar
from .editar import Editar2
from .acerca_de import Acerca_de
from .informacion_medios import Informacion_medios

traductor = Traductor()
_ = traductor._


class Frame(wx.Frame):
    def __init__(self, parent, title, controlador, app, opciones):
        super().__init__(parent, title=title, style=wx.DEFAULT_FRAME_STYLE | wx.MAXIMIZE)
        self.syze = (800, 800)
        self.controlador = controlador
        self.controlador_app = app
        self.controlador_opciones = opciones
        self.Center()
        self.alertar_instancia()
        self.graficar()
        self.Show()

    # creación de controles
    def graficar(self):
        # creación de lector
        self.lector = accessible_output2.outputs.auto.Auto()

        # ID personalizados
        self.id_bt_enfocar_lista = wx.NewIdRef()
        self.id_bt_enfocar_linea_tiempo = wx.NewIdRef()
        self.id_bt_tiempo_actual = wx.NewIdRef()
        self.id_hablar_duracion = wx.NewIdRef()
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
        self.barrademenu = wx.MenuBar()
        self.SetMenuBar(self.barrademenu)

    # creación del menú archivo
        menu1 = wx.Menu()
        self.barrademenu.Append(menu1, _('&Archivo'))
        self.mn_nuevo_proyecto = menu1.Append(self.id_mn_nuevo_proyecto, _('&Nuevo proyecto') + ' \tCtrl + n')
        self.mn_nuevo_proyecto.Enable(False)
        self.Bind(wx.EVT_MENU, self.crear_proyecto, self.mn_nuevo_proyecto)
        self.atajo_mn_nuevo_proyecto = wx.AcceleratorEntry(wx.ACCEL_CTRL, ord('n'), self.id_mn_nuevo_proyecto)
        self.mn_cargar_audio = menu1.Append(-1, _('&Cargar audio'))
        self.Bind(wx.EVT_MENU, self.abrir_archivo, self.mn_cargar_audio)
        self.mn_abrir_proyecto = menu1.Append(self.id_mn_abrir_proyecto, _('&Abrir proyecto') + '\tCtrl+O')
        self.Bind(wx.EVT_MENU, self.abrir_proyecto, self.mn_abrir_proyecto)
        self.atajo_abrir_proyecto = wx.AcceleratorEntry(wx.ACCEL_CTRL, ord('o'), self.id_mn_abrir_proyecto)
        self.mn_guardar = menu1.Append(self.id_mn_guardar, _('&Guardar') + '\tCtrl+S')
        self.mn_guardar.Enable(False)
        self.Bind(wx.EVT_MENU, self.guardar, self.mn_guardar)
        self.mn_guardar_como = menu1.Append(-1, _('G&uardar como...'))
        self.mn_guardar_como.Enable(False)
        self.Bind(wx.EVT_MENU, self.guardar_proyecto, self.mn_guardar_como)
        self.sub_mn_exportar = wx.Menu()
        self.mn_exportar = menu1.AppendSubMenu(self.sub_mn_exportar, _('&Exportar'))
        self.mn_exportar.Enable(False)
        self.mn_exportar_cue = self.sub_mn_exportar.Append(-1, _('&Imagen CUE'))
        self.Bind(wx.EVT_MENU, self.exportar_cue, self.mn_exportar_cue)
        self.mn_exportar_pistas_separadas = self.sub_mn_exportar.Append(-1, _('&Pistas separadas'))
        self.Bind(wx.EVT_MENU, self.exportar_pistas_separadas, self.mn_exportar_pistas_separadas)
        salir = menu1.Append(-1, _('&Salir'))
        self.Bind(wx.EVT_MENU, self.cerrar, salir)

        ''' creacion del menu editar '''
        menu2 = wx.Menu()
        self.mn_editar = self.barrademenu.Append(menu2, _('&Editar'))
        self.mn_deshacer = menu2.Append(self.id_mn_deshacer, _('&Deshacer') + '\tCtrl+Z')
        self.mn_deshacer.Enable(False)
        self.Bind(wx.EVT_MENU, self.deshacer, self.id_mn_deshacer)
        self.atajo_deshacer = wx.AcceleratorEntry(wx.ACCEL_CTRL, ord('z'), self.id_mn_deshacer)
        self.mn_rehacer = menu2.Append(self.id_mn_rehacer, _('&Rehacer') + '\tCtrl+Shift+Z')
        self.Bind(wx.EVT_MENU, self.rehacer, self.id_mn_rehacer)
        self.mn_rehacer.Enable(False)
        self.atajo_rehacer = wx.AcceleratorEntry(wx.ACCEL_CTRL | wx.ACCEL_SHIFT, ord('z'), self.id_mn_rehacer)
        self.mn_eliminar = menu2.Append(-1, _('&Eliminar') + '\tSupr')
        self.Bind(wx.EVT_MENU, self.borrar_item, self.mn_eliminar)
        self.mn_eliminar.Enable(False)
        self.mn_marca = menu2.Append(self.id_mn_editar_marca, _('&Marca') + '\tCtrl+e')
        self.Bind(wx.EVT_MENU, self.editar_marca, self.id_mn_editar_marca)
        self.mn_marca.Enable(False)
        self.atajo_editar_marca = wx.AcceleratorEntry(wx.ACCEL_CTRL, ord('e'), self.id_mn_editar_marca)

        ''' creación del menú herramientas '''
        menu3 = wx.Menu()
        self.barrademenu.Append(menu3, _('&Herramientas'))
        self.mn_metadatos_disco = menu3.Append(self.id_mn_metadatos_disco, _('&Metadatos del álbum') + '\tCtrl+Shift+M')
        self.mn_metadatos_disco.Enable(False)
        self.Bind(wx.EVT_MENU, self.guardar_disco, self.mn_metadatos_disco)
        self.atajo_metadatos_disco = wx.AcceleratorEntry(wx.ACCEL_CTRL | wx.ACCEL_SHIFT, ord('m'), self.id_mn_metadatos_disco)
        self.mn_informacion = menu3.Append(self.id_mn_informacion, _('&Información de medios') + '\tCtrl+I')
        self.Bind(wx.EVT_MENU, self.informar_medios, self.id_mn_informacion)
        self.atajo_informacion = wx.AcceleratorEntry(wx.ACCEL_CTRL, ord('i'), self.id_mn_informacion)
        self.mn_informacion.Enable(False)
        self.mn_opciones = menu3.Append(self.id_mn_opciones, _('&Opciones') + '\tCtrl+P')
        self.Bind(wx.EVT_MENU, self.abrir_opciones, self.mn_opciones)
        self.atajo_opciones = wx.AcceleratorEntry(wx.ACCEL_CTRL, ord('p'), self.id_mn_opciones)

        ''' creación del menú ayuda '''
        menu4 = wx.Menu()
        self.barrademenu.Append(menu4, _('A&yuda'))
        self.mn_documentacion = menu4.Append(self.id_mn_documentacion, _('&Documentación') + '\tF1')
        self.Bind(wx.EVT_MENU, self.abrir_documentacion, self.mn_documentacion)
        self.atajo_documentacion = wx.AcceleratorEntry(wx.ACCEL_NORMAL, wx.WXK_F1, self.id_mn_documentacion)
        self.mn_novedades = menu4.Append(-1, _('&Novedades'))
        self.Bind(wx.EVT_MENU, self.abrir_novedades, self.mn_novedades)
        self.mn_buscar_actualizacion = menu4.Append(-1, _('&Buscar actualizaciones'))
        self.Bind(wx.EVT_MENU, self.buscar_actualizacion, self.mn_buscar_actualizacion)
        self.mn_registro = menu4.Append(-1, _('&Registro'))
        self.Bind(wx.EVT_MENU, self.abrir_registro, self.mn_registro)
        acercade = menu4.Append(-1, _('Acerca de ') + self.controlador_app.nombre_app)
        self.Bind(wx.EVT_MENU, self.mg_acerca, acercade)

        ''' panel y controles '''
        self.panel1 = wx.Panel(self)
        self.panel2 = wx.Panel(self.panel1)
        self.l_abrir = wx.StaticText(self.panel1, -1, _('Carga el archivo de audio que quieres procesar.'))
        self.bt_abrir = wx.Button(self.panel1, -1, _('&Cargar audio'))
        self.bt_abrir.SetFocus()
        self.Bind(wx.EVT_BUTTON, self.abrir_archivo, self.bt_abrir)
        backend = wx.media.MEDIABACKEND_DIRECTSHOW
        self.reproductor = wx.media.MediaCtrl()
        self.reproductor.Create(self.panel2, style=wx.SIMPLE_BORDER, szBackend=backend)
        self.reproductor.Show(False)

        self.l_encabezado = wx.StaticText(self.panel2, -1, _('Nuevo proyecto'))
        self.font_encabezado = self.l_encabezado.GetFont()
        self.font_encabezado.SetPointSize(30)
        self.l_encabezado.SetFont(self.font_encabezado)
        self.valores = '0:0:0:0'
        self.l_reloj = wx.StaticText(self.panel2, -1, self.valores)
        self.font_reloj = self.l_reloj.GetFont()
        self.font_reloj.SetPointSize(60)
        self.l_reloj.SetFont(self.font_reloj)
        self.l_pista = wx.StaticText(self.panel2, -1, _('Línea de tiempo'))
        self.minutaje = 1
        self.linea_tiempo = wx.Slider(self.panel2, -1, self.controlador.reproductor.tiempo_actual, 0, self.minutaje, size=(400, -1))
        self.linea_tiempo.SetLineSize(5000)
        self.linea_tiempo.SetPageSize(60000)

        self.Bind(wx.EVT_SLIDER, self.mover, self.linea_tiempo)
        self.bt_reproducir = wx.Button(self.panel2, -1, _('&Reproducir'))
        self.Bind(wx.EVT_BUTTON, self.reproducir_pausar, self.bt_reproducir)
        self.Bind(wx.media.EVT_MEDIA_STOP, self.detener, self.reproductor)
        self.timer = wx.Timer(self)
        self.timer.Start(self.reproductor.Length())
        self.Bind(wx.EVT_TIMER, self.temporizar)

        self.bt_enfocar_linea_tiempo = wx.Button(self.panel2, self.id_bt_enfocar_linea_tiempo, _('línea de tiempo'))
        self.bt_enfocar_linea_tiempo.Show(False)
        self.Bind(wx.EVT_BUTTON, self.enfocar_linea_tiempo, self.id_bt_enfocar_linea_tiempo)
        self.atajo_enfocar_linea_tiempo = wx.AcceleratorEntry(wx.ACCEL_CTRL, ord('l'), self.id_bt_enfocar_linea_tiempo)
        self.bt_enfocar_lista = wx.Button(self.panel2, self.id_bt_enfocar_lista, _('enfocar lista'))
        self.bt_enfocar_lista.Show(False)
        self.Bind(wx.EVT_BUTTON, self.enfocar_lista, self.id_bt_enfocar_lista)
        self.atajo_enfocar_lista = wx.AcceleratorEntry(wx.ACCEL_CTRL, ord('m'), self.id_bt_enfocar_lista)
        self.bt_duracion = wx.Button(self.panel2, self.id_hablar_duracion, _('Duración'))
        self.bt_duracion.Show(False)
        self.Bind(wx.EVT_BUTTON, self.hablar_duracion, self.id_hablar_duracion)
        self.atajo_duracion = wx.AcceleratorEntry(wx.ACCEL_CTRL, ord('d'), self.id_hablar_duracion)
        self.bt_tiempo_actual = wx.Button(self.panel2, self.id_bt_tiempo_actual, _('tiempo actual'))
        self.bt_tiempo_actual.Show(False)
        self.Bind(wx.EVT_BUTTON, self.hablar_tiempo_actual, self.id_bt_tiempo_actual)
        bt_detener = wx.Button(self.panel2, -1, _('&Detener'))
        self.Bind(wx.EVT_BUTTON, self.detener, bt_detener)
        wx.StaticText(self.panel2, -1, _('Volumen'))
        self.volumen = wx.Slider(self.panel2, -1, self.controlador.reproductor.volumen * 100, 0, 100)
        self.Bind(wx.EVT_SLIDER, self.volumenear, self.volumen)
        self.bt_marcar = wx.Button(self.panel2, -1, _('&Marcar'))
        self.bt_marcar.Enable(False)
        self.Bind(wx.EVT_BUTTON, self.marcar, self.bt_marcar)
        self.atajo_tiempo_actual = wx.AcceleratorEntry(wx.ACCEL_CTRL, ord('t'), self.id_bt_tiempo_actual)
        self.entradas_atajos = [self.atajo_enfocar_lista, self.atajo_enfocar_linea_tiempo, self.atajo_tiempo_actual, self.atajo_duracion, self.atajo_deshacer, self.atajo_rehacer, self.atajo_mn_nuevo_proyecto, self.atajo_abrir_proyecto, self.atajo_metadatos_disco, self.atajo_opciones, self.atajo_documentacion, self.atajo_editar_marca, self.atajo_informacion]
        self.tabla_atajos = wx.AcceleratorTable(self.entradas_atajos)
        self.SetAcceleratorTable(self.tabla_atajos)

        self.Bind(wx.EVT_CLOSE, self.cerrar)
# Construcción de lista
        self.l_lista = wx.StaticText(self.panel2, -1, _('Marcas'))
        self.lista = wx.ListCtrl(self.panel2, -1, style=wx.LC_REPORT | wx.LC_VRULES | wx.LC_SINGLE_SEL)
        self.lista.InsertColumn(0, 'N°')
        self.lista.InsertColumn(1, _('Título'))
        self.lista.InsertColumn(2, _('Autor'))
        self.lista.InsertColumn(3, _('Tiempo de inicio'))
        self.Bind(wx.EVT_LIST_KEY_DOWN, self.detectar_tecla_lista, self.lista)
        self.Bind(wx.EVT_LIST_ITEM_RIGHT_CLICK, self.desplegar_contextual, self.lista)
        self.Bind(wx.EVT_LIST_ITEM_FOCUSED, self.posicionar_marca, self.lista)
#        self.Bind(wx.EVT_LIST_ITEM_SELECTED, self.seleccionar_multiple, self.lista)
        self.l_formato = wx.StaticText(self.panel2, -1, _('Modo de exportación'))
        self.lista_formatos = [_('Imagen CUE'), _('Pistas separadas')]
        self.com_modo = wx.ComboBox(self.panel2, -1, _('Imagen CUE'), choices=self.lista_formatos, style=wx.CB_READONLY)
        self.com_modo.Enable(False)
        self.Bind(wx.EVT_COMBOBOX, self.seleccionar_modo, self.com_modo)
        self.bt_opciones = wx.Button(self.panel2, -1, _('&Opciones'))
        self.Bind(wx.EVT_BUTTON, self.abrir_opciones, self.bt_opciones)
        self.bt_opciones.Enable(False)
        self.bt_exportar = wx.Button(self.panel2, -1, _('E&XPORTAR'))
        self.bt_exportar.Enable(False)
        self.Bind(wx.EVT_BUTTON, self.exportar, self.bt_exportar)


# creación de sizers

        self.sz0 = wx.BoxSizer(wx.VERTICAL)
        self.sz0.Add(self.l_abrir)
        self.sz0.Add(self.bt_abrir)
        self.sz0.Add(self.panel2, wx.SizerFlags().Expand())
        self.panel1.SetSizer(self.sz0)

        self.sz1 = wx.BoxSizer(wx.VERTICAL)

        self.sz1.Add(self.l_encabezado, wx.SizerFlags().Center())
        self.sz1.Add(self.l_reloj, wx.SizerFlags().Center())
        self.sz1.Add(self.reproductor)

        self.sz1.Add(self.linea_tiempo, wx.SizerFlags().Expand())

        self.sz2 = wx.BoxSizer(wx.HORIZONTAL)
        self.sz1.Add(self.sz2)
        self.sz2.Add(self.bt_reproducir)
        self.sz2.Add(bt_detener)
        self.sz2.Add(self.volumen)
        self.sz2.Add(self.bt_marcar)

        self.sz3 = wx.BoxSizer(wx.HORIZONTAL)
        self.sz1.Add(self.sz3, flag=wx.ALL | wx.CENTER)
        self.sz3.Add(self.lista, flag=wx.ALL | wx.CENTER)

        self.sz4 = wx.BoxSizer(wx.VERTICAL)
        self.sz3.Add(self.sz4)
        self.sz4.Add(self.com_modo)
        self.sz4.Add(self.bt_opciones)
        self.sz4.Add(self.bt_exportar)

        self.panel2.SetSizer(self.sz1)
        self.panel2.Enable(False)

        ''' llamado a funciones '''
        self.detectar_actualizacion()

    def listar(self):
        ''' carga marcas en  la lista '''
        id = self.lista.GetItemCount()
        for marca in self.controlador.getMarcas():
            self.lista.InsertItem(id, str(marca.id))
            self.lista.SetItem(id, 1, marca.titulo)
            self.lista.SetItem(id, 2, marca.autor)
            self.lista.SetItem(id, 3, marca.tiempo_inicio)
            id += 1

    def refrescar_principal(self):
        ''' Refresca la interfáz principal. '''
        self.lista.DeleteAllItems()
        self.panel1.Destroy()
        self.graficar()
        self.Show()
        self.Layout()
        if self.controlador.pista is not None:
            self.reproductor.Load(self.controlador.pista.ruta)
        self.habilitar_controles()
        self.desactivar_controles()

    def refrescar_lista(self):
        self.lista.DeleteAllItems()
        self.listar()

    def detectar_tecla_lista(self, event):
        ''' Detecta qué tecla se a presionado sobre un elemento de la lista de marcas. '''
        tecla = event.GetKeyCode()
        if tecla == wx.WXK_DELETE:
            self.borrar_item(None)
        elif tecla == wx.WXK_WINDOWS_MENU:
            self.desplegar_contextual(event)

    def posicionar_marca(self, event):
        ''' Posiciona el inicio de reproducción según el tiempo de inicio de cada marca '''
        item = self.lista.GetFocusedItem()
        self.controlador.reproductor.marca_id = item
        marca = self.controlador.getMarcas()[item]
        self.reproductor.Seek(marca.milesimas)

    def borrar_item(self, event):
        ''' Elimina las marcas seleccionadas en la lista '''
        item = self.lista.GetFocusedItem()
        cantidad = self.lista.GetItemCount()
        for marca in reversed(range(cantidad)):
            sl = self.lista.IsSelected(marca)
            if sl is True:
                self.controlador.borrar_marca(marca)
        self.refrescar_lista()
        self.lista.SetItemState(item - 1, wx.LIST_STATE_FOCUSED, wx.LIST_STATE_FOCUSED)
        self.lista.EnsureVisible(item - 1)
        if cantidad != 0:
            logging.info(_('marca eliminada.'))
            self.lector.output(_('Eliminado'))

    def desplegar_contextual(self, event):
        ''' Despliega el menú contextual de la lista de marcas '''
        self.PopupMenu(Contextual(self))

    def cerrar(self, event):
        self.controlador_opciones.guardar_opciones('general', 'idioma', str(self.controlador_opciones.modelo_configuracion.idioma_app))
        if self.controlador.pista is not None:
            self.detectar_cambios()
            self.controlador.limpiar_temporal()
            self.timer.Stop()
            self.Destroy()
            logging.info(_('Finalizada la ejecución de Labrandeos.'))
        else:
            self.controlador.limpiar_temporal()
            self.Destroy()
            logging.info(_('Finalizada la ejecución de Labrandeos.'))

    def guardar_disco(self, event):
        ''' Abre el diálogo para guardar los metadatos del disco. '''
        self.vn_disco = vista.disco.Disco(self, _('Metadatos del álbum'), self.controlador)
        if self.vn_disco.ShowModal() == wx.ID_OK:
            self.controlador.crear_disco(
                self.vn_disco.getTitulo(),
                self.vn_disco.getAutor(),
                self.vn_disco.getFecha(),
                self.vn_disco.getGenero(),
                self.vn_disco.getComentarios()
            )
            self.mn_metadatos_disco.Enable(True)
            self.mn_deshacer.Enable(True)
            self.vn_disco.guardar_datos()
            self.cambiar_encabezado()
        else:
            self.cambiar_encabezado()

    def cambiar_encabezado(self):
        if self.controlador.data.titulo != '' and self.controlador.data.autor == '':
            self.l_encabezado.SetLabel(f'{self.controlador.data.titulo} - {_("Sin autor")}')
        elif self.controlador.data.titulo == '' and self.controlador.data.autor != '':
            self.l_encabezado.SetLabel(f'{_("Sin título")} - {self.controlador.data.autor}')
        elif self.controlador.data.titulo != '' and self.controlador.data.autor != '':
            self.l_encabezado.SetLabel(f'{self.controlador.data.titulo} - {self.controlador.data.autor}')
        else:
            self.l_encabezado.SetLabel(f'{_("Sin título")} - {_("Sin autor")}')

    def abrir_archivo(self, event):
        ''' Abre la ventana de diálogo para cargar un archivo de audio al proyecto. '''
        self.dialogo = wx.FileDialog(self, _('Cargar audio'), style=wx.FD_OPEN)
        if self.dialogo.ShowModal() == wx.ID_OK:
            self.path = self.dialogo.GetPath()
            tipo_archivo = self.controlador.comprobar_medios(self.path)
            if tipo_archivo is None or tipo_archivo[0] != 'audio':
                wx.MessageBox(_('No es posible cargar el fichero, sólo se admiten archivos de audio.'), caption='Atención', style=wx.ICON_ERROR)
                logging.warning(_('Se intenta cargar un archivo que no es de audio.'))
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
            self.reproductor.Length()
        )
        self.controlador.aplicar_informacion_medios(self.path)

    def habilitar_controles(self):
        if self.controlador.pista is not None:
            self.panel2.Enable(True)
            self.mn_metadatos_disco.Enable(True)
            self.mn_informacion.Enable(True)
            self.mn_nuevo_proyecto.Enable(True)
            self.mn_deshacer.Enable(True)
            self.bt_marcar.Enable(True)
        if self.controlador.data is not None:
            self.mn_exportar.Enable(True)
            self.mn_guardar.Enable(True)
            self.atajo_guardar = wx.AcceleratorEntry(wx.ACCEL_CTRL, ord('s'), self.id_mn_guardar)
            self.entradas_atajos.append(self.atajo_guardar)
            self.mn_guardar_como.Enable(True)
            self.com_modo.Enable(True)
            self.bt_exportar.Enable(True)
        if self.controlador.data is not None and self.controlador.data.lista_marcas != []:
            self.mn_eliminar.Enable(True)
            self.mn_marca.Enable(True)

    def desactivar_controles(self):
        ''' desactiva controles '''
        if self.controlador.pista is not None:
            self.bt_abrir.Enable(False)
            self.mn_cargar_audio.Enable(False)

    def abrir_proyecto(self, event):
        ''' abre un proyecto existente '''
        self.dialogo_abrir_proyecto = wx.FileDialog(self, _('Abrir proyecto'), style=wx.FD_OPEN, wildcard='*.lap')
        if self.dialogo_abrir_proyecto.ShowModal() == wx.ID_OK:
            mensaje = 0
            if self.controlador.pista is not None:
                mensaje = wx.MessageBox(_('Estás a punto de abrir un nuevo proyecto. Los cambios que hayas hecho se perderán. \n ¿Deseas continuar?'), _('Atención'), style=wx.OK | wx.CANCEL | wx.CANCEL_DEFAULT | wx.ICON_EXCLAMATION)
            if self.controlador.pista is None or mensaje == 2:
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
        if self.controlador.comparar_modelo() is not True:
            mensaje = wx.MessageBox(_('¿Deseas guardar los cambios realizados?'), _('Guardar'), style=wx.YES_NO | wx.CANCEL | wx.YES_DEFAULT | wx.ICON_QUESTION)
            if mensaje == wx.YES and self.controlador.es_temporal() is True:
                logging.info(_('El usuario acepta guardar los cambios realizados. Se inicia el guardado en un nuevo proyecto.'))
                self.guardar_proyecto(None)
            elif mensaje == wx.YES and self.controlador.es_temporal() is False:
                logging.info(_('El usuario acepta guardar los cambios realizados en el proyecto existente.'))
                self.guardar(None)
            elif mensaje == wx.CANCEL:
                logging.info(_('El usuario no acepta guardar los cambios realizados al proyecto.'))
                raise Exception('Cancelado')

    def crear_proyecto(self, event):
        ''' Crea un nuevo proyecto '''
        self.detectar_cambios()
        self.controlador.limpiar_temporal()
        self.path = ''
        self.controlador.crear_proyecto()
        self.controlador.save()
        self.controlador.limpiar_proyecto()
#        self.habilitar_controles()
        self.refrescar_principal()
        self.lector.output(_('Nuevo proyecto'))

    def guardar(self, event):
        ''' guardar cambios en proyecto actual '''
        if os.path.basename(self.controlador.ruta_proyecto) == 'temp.proyecto.lap':
            self.guardar_proyecto(None)
        else:
            self.controlador.save()
            self.lector.output(_('guardado'))

    def guardar_proyecto(self, event):
        ''' guarda el proyecto en una ruta específica '''
        self.dialogo_guardar = wx.FileDialog(self, _('Guardar proyecto'), style=wx.FD_SAVE, wildcard='*.lap')
        if self.dialogo_guardar.ShowModal() == wx.ID_OK:
            if os.path.isfile(self.dialogo_guardar.GetPath()):
                logging.warning(_('El directorio en el cual se intenta guardar el proyecto, ya contiene un archivo con el mismo nombre.'))
                mensaje = wx.MessageBox(_('Ya existe un fichero con este nombre. ¿Deseas reemplazarlo?'), _('Atención'), style=wx.YES_NO | wx.NO_DEFAULT | wx.ICON_EXCLAMATION)
                if mensaje == 2:
                    logging.info(_('El usuario acepta sobreescribir el proyecto del mismo nombre.'))
                    self.controlador.ruta_proyecto = self.dialogo_guardar.GetPath()
                    self.controlador.save()
                    self.controlador.limpiar_temporal()
            else:
                self.controlador.ruta_proyecto = self.dialogo_guardar.GetPath()
                self.controlador.save()
                self.controlador.limpiar_temporal()
        else:
            raise Exception('Cancelado')
        logging.info(_('El usuario no acepta sobreescribir el archivo existente del proyecto con el mismo nombre.'))

    def abrir_opciones(self, event):
        ''' abre la ventana de opciones '''
        self.vn_opciones = vista.opciones.Opciones(self, _('Opciones'), opciones=self.controlador_opciones)
        evento = event.GetEventObject()
        if isinstance(evento, wx.Button):
            self.vn_opciones.libreta.SetSelection(1)
        idioma_anterior = self.vn_opciones.pagina1.com_idioma.GetValue()
        if self.vn_opciones.ShowModal() == wx.ID_OK:
            self.vn_opciones.pagina1.guardar_opciones()
            self.vn_opciones.pagina2.guardar_opciones()
            idioma_posterior = self.vn_opciones.pagina1.com_idioma.GetValue()
            if idioma_anterior != idioma_posterior:
                wx.MessageBox(_('Debes reiniciar el programa para que los cambios de idioma surtan efecto.'), _('Atención'), style=wx.ICON_EXCLAMATION)

    def abrir_documentacion(self, event):
        if self.controlador_opciones.consultar_opciones('str', 'general', 'idioma') == 'es':
            os.startfile(os.path.join('files', 'documentation', 'help', 'es.html'))
        else:
            os.startfile(os.path.join('files', 'documentation', 'help', 'en.html'))

    def abrir_novedades(self, event):
        ''' Abre el documento con las novedades. '''
        if self.controlador_opciones.consultar_opciones('str', 'general', 'idioma') == 'es':
            os.startfile(os.path.join('files', 'documentation', 'news', 'es.html'))
        else:
            os.startfile(os.path.join('files', 'documentation', 'news', 'en.html'))

    def abrir_registro(self, event):
        ''' Abre el registro de eventos (log). '''
        os.startfile(os.path.join(os.environ['LOCALAPPDATA'], 'Labrandeos', 'labrandeos.log'))

    def alertar_instancia(self):
        ''' Muestra alerta si se abre una nueva instancia del programa '''
        if self.controlador_app.verificar_instancia():
            wx.MessageBox(f'{self.controlador_app.nombre_app} {_("ya se está ejecutando.")}', _('Aviso'), style=wx.ICON_INFORMATION)
            sys.exit(1)

    def detectar_actualizacion(self):
        if self.controlador_opciones.consultar_opciones('bool', 'general', 'detectar_actualizacion'):
            self.buscar_actualizacion(None)

    def buscar_actualizacion(self, event):
        ''' Muestra mensajes si hay o no actualizaciones '''
        self.controlador_app.verificarNuevaVersion()
        if self.controlador_app.actualizado is False:
            if self.controlador_opciones.consultar_opciones('bool', 'general', 'sonido_actualizacion'):
                wx.adv.Sound.PlaySound(os.path.join('files', 'sounds', 'nueva_version.wav'))
            res = wx.MessageBox(_('Hay una nueva versión disponible. ¿Deseas descargarla ahora?'), _('Actualización'), style=wx.YES_NO | wx.ICON_ASTERISK)
            if res == wx.YES:
                self.controlador_app.descargar_version()
        elif self.controlador_app.actualizado is True and event is not None:
            wx.MessageBox(_('No hay ninguna nueva versión disponible'), _('Aviso'), style=wx.ICON_INFORMATION)

# muestra información acerca del programa
    def mg_acerca(self, event):
        dlg = Acerca_de(self, title=_('Acerca de ') + self.controlador_app.nombre_app)
        if dlg.ShowModal() == wx.ID_OK:
            dlg.close()

    def enfocar_linea_tiempo(self, event):
        self.linea_tiempo.SetFocus()

    def enfocar_lista(self, event):
        self.lista.SetFocus()

    def reproducir_pausar(self, event):
        ''' Reproduce o pausa la pista. '''
        self.estado = self.reproductor.GetState()
        if self.estado == 1 or self.estado == 0:
            self.reproductor.Play()
            self.bt_reproducir.SetLabel(_('&Pausar'))
            self.minutaje = self.reproductor.Length()
            self.linea_tiempo.SetMax(self.minutaje)
        elif self.estado == 2:
            self.reproductor.Pause()
            self.bt_reproducir.SetLabel(_('&Reproducir'))

    def pausar(self, event):
        ''' pausa la reproducción. '''
        self.estado = self.reproductor.GetState()
        if self.estado == 2:
            self.reproductor.Pause()
            self.bt_reproducir.SetLabel(_('&Reproducir'))

    def detener(self, event):
        ''' detiene la reproducción. '''
        self.estado = self.reproductor.GetState()
        if self.estado == 1 or self.estado == 2:
            self.reproductor.Stop()
            self.bt_reproducir.SetLabel(_('&Reproducir'))
        else:
            self.bt_reproducir.SetLabel(_('&Reproducir'))

    def volumenear(self, event):
        ''' controla el volumen. '''
        a = self.volumen.GetValue()
        b = a / 100
        self.reproductor.SetVolume(b)
        self.controlador.reproductor.volumen = b

    def mover(self, event):
        ''' busca un momento de la pista cuando el usuario mueve la aguja del control. '''
        self.reproductor.Seek(self.linea_tiempo.GetValue())

    def temporizar(self, event):
        ''' mueve la aguja del control de la pista de forma automática a medida que se reproduce el audio. '''
        self.tiempo = self.reproductor.Tell()
        self.linea_tiempo.SetValue(self.tiempo)
        valores = self.calcular_tiempo(self.tiempo)
        str_valores = []
        for i in valores:
            v = str(i)
            c_v = len(v)
            if c_v == 1:
                v = '0' + v
            str_valores.append(v)
        valores = ' : '.join(str_valores)
        self.l_reloj.SetLabel(valores)
        if self.controlador.pista is not None:
            self.controlador.reproductor.tiempo_actual = self.tiempo

    def calcular_tiempo(self, tiempo):
        ''' calcula y muestra el tiempo de la pista en horas,minutos,segundos y marcos. '''
        milesimas = int(tiempo * 75 / 1000)  # convierte milésimas a cantidad de marcos
        self.marcos = milesimas % 75
        self.segundos = int(milesimas / 75 % 60)
        self.minutos = int(milesimas / 60 / 75 % 60)
        self.full_minutos = int(milesimas / 60 / 75)
        self.horas = int(milesimas / 60 / 60 / 75)
        self.valores = (self.horas, self.minutos, self.segundos, self.marcos)
        return self.valores

    def formatear_tiempo(self, horas, minutos, segundos, marcos):
        ''' Devuelve el tiempo formateado '''
        horas = '{}'.format(str(horas) + _('horas') if horas != 1 else _('una hora'))
        minutos = '{}'.format(str(minutos) + _('minutos') if minutos != 1 else _('un minuto'))
        segundos = '{}'.format(str(segundos) + _('segundos') if segundos != 1 else _('un segundo'))
        marcos = '{}'.format(str(marcos) + _('marcos') if marcos != 1 else _('un marco'))
        return '{} {} {} {}'. format(horas if self.horas != 0 else '', minutos if self.minutos != 0 else '', segundos if self.segundos != 0 else '', marcos if self.marcos != 0 else '')

    def hablar_tiempo_actual(self, event):
        ''' verbaliza el tiempo actual de la pista '''
        self.lector.output(self.formatear_tiempo(self.horas, self.minutos, self.segundos, self.marcos))

    def hablar_duracion(self, event):
        ''' verbaliza el tiempo de duración del archivo de audio. '''
        self.duracion = self.reproductor.Length()
        valores = self.calcular_tiempo(self.duracion)
        self.lector.output(_('Duración de la pista. ') + self.formatear_tiempo(valores[0], valores[1], valores[2], valores[3]))

    def marcar(self, event):
        self.reproductor.Pause()
        self.bt_reproducir.SetLabel(_('&Reproducir'))
        if self.controlador_opciones.consultar_opciones('bool', 'general', 'sonido_marca'):
            wx.adv.Sound.PlaySound(os.path.join('files', 'sounds', 'marca.wav'))
        self.vn_editar()

    def vn_editar(self):
        self.editar = Editar(self, _('Crear marca'), self.controlador, self.reproductor)
        self.editar.getTiempo(self.reproductor.Tell())
        self.editar.tiempo_actual = self.reproductor.Tell()
        self.editar.duracion_tiempo = self.calcular_tiempo(self.reproductor.Length())
        if self.editar.ShowModal() == wx.ID_OK:
            self.pausar(None)
            marca = self.controlador.crearMarca(
                self.lista.GetItemCount(),
                self.editar.getTitulo(),
                self.editar.getAutor(),
                self.editar.getTiempoInicio(),
                self.editar.tiempo_actual
            )
            id = self.lista.GetItemCount()
            self.lista.InsertItem(id, str(marca.id))
            self.lista.SetItem(id, 1, marca.titulo)
            self.lista.SetItem(id, 2, marca.autor)
            self.lista.SetItem(id, 3, marca.tiempo_inicio)
            self.refrescar_lista()
            self.habilitar_controles()
        else:
            self.pausar(None)

    def editar_marca(self, event):
        self.editar2 = Editar2(self, _('Editar marca'), self.controlador, self.reproductor)
        self.pausar(None)
        item = self.lista.GetFocusedItem()
        marca = self.controlador.consultar_datos(item)
        self.editar2.getTiempo(marca.milesimas)
        item_enfocado = self.lista.GetFocusedItem()
        if self.editar2.ShowModal() == wx.ID_OK:
            self.pausar(None)
            marca = self.controlador.editarMarca(
                item,
                self.editar2.getTitulo(),
                self.editar2.getAutor(),
                self.editar2.getTiempoInicio(),
                self.editar2.tiempo_actual
            )
            self.lista.SetItem(item, 0, str(marca.id))
            self.lista.SetItem(item, 1, marca.titulo)
            self.lista.SetItem(item, 2, marca.autor)
            self.lista.SetItem(item, 3, marca.tiempo_inicio)
            self.refrescar_lista()
            self.habilitar_controles()
            self.lista.Focus(item_enfocado)
        else:
            self.pausar(None)

    def seleccionar_modo(self, event):
        ''' maneja controles y funciones según modo seleccionado de exportación. '''
        if self.com_modo.GetValue() == _('Pistas separadas'):
            self.bt_opciones.Enable(True)
        else:
            self.bt_opciones.Enable(False)

    def exportar(self, event):
        if self.com_modo.GetValue() == _('Imagen CUE'):
            self.exportar_cue(event)
        elif self.com_modo.GetValue() == _('Pistas separadas'):
            self.exportar_pistas_separadas(event)

    def exportar_cue(self, event):
        ''' Exporta en formato cue. '''
        logging.info(_('Inicia la exportación del proyecto como imagen CUE.'))
        ruta_exportacion = self.controlador.exportar_cue(self.controlador_opciones.consultar_opciones('bool', 'general', 'indice'))
        self.alertar_exportacion(ruta_exportacion)
        logging.info(_('Finaliza exportación del Proyecto como imagen CUE'))

    def exportar_pistas_separadas(self, event):
        ''' Exporta audio como pistas separadas. '''
        logging.info(_('Inicia la exportación del proyecto como pistas de audio separadas.'))
        ruta_exportacion = self.seleccionar_carpeta_exportacion()
        if ruta_exportacion:
            ruta_final = os.path.join(ruta_exportacion, f'{self.controlador.data.titulo} - {self.controlador.data.autor}')
            self.iniciar_progreso_exportacion(len(self.controlador.getMarcas()))
            self.controlador.dividir_audio(self.controlador_opciones.consultar_todas_opciones(), ruta_exportacion, self.actualizar_progreso_exportacion)
            self.alertar_exportacion(ruta_final)
            logging.info(_('Finaliza la exportación del proyecto como pistas de audio separadas.'))

    def alertar_exportacion(self, ruta_final):
        ''' Muestra alerta y sonido al finalizar la exportación. '''
        if self.controlador_opciones.consultar_opciones('bool', 'general', 'sonido_exportar'):
            wx.adv.Sound.PlaySound(os.path.join('files', 'sounds', 'ok.wav'))
        if self.controlador_opciones.consultar_opciones('bool', 'general', 'ABRIR_CARPETA'):
            subprocess.Popen(f'explorer /select,"{ruta_final}"')
        if self.controlador_opciones.consultar_opciones('bool', 'general', 'sonido_exportar') is False and self.controlador_opciones.consultar_opciones('bool', 'general', 'ABRIR_CARPETA') is False:
            msg = wx.adv.NotificationMessage('', _('Cue exportado exitosamente.'), self, wx.ICON_INFORMATION)
            msg.Show(5)

    def seleccionar_carpeta_exportacion(self):
        ''' Abre un diálogo para seleccionar la carpeta de destino al exportar pistas de audio separadas. '''
        dialogo = wx.DirDialog(self, _('Selecciona la carpeta de destino'))
        if dialogo.ShowModal() == wx.ID_OK:
            nombre_carpeta = f'{self.controlador.data.titulo} - {self.controlador.data.autor}'
            ruta_destino = dialogo.GetPath()
            ruta_carpeta = os.path.join(ruta_destino, nombre_carpeta)
            if os.path.exists(ruta_carpeta):
                logging.warning(_('Se intenta exportar en un directorio que ya contiene una carpeta con el mismo nombre del proyecto.'))
                mensaje = wx.MessageBox(_('Ya existe una carpeta con el mismo nombre. ¿Deseas reemplazarla?'), _('Atención'), style=wx.YES_NO | wx.NO_DEFAULT | wx.ICON_EXCLAMATION)
                if mensaje == wx.NO:
                    return None
                elif mensaje == wx.YES:
                    logging.info(_('El usuario acepta  sobreescribir la carpeta con el mismo nombre del proyecto.'))
                    return ruta_destino
            else:
                return ruta_destino

    def iniciar_progreso_exportacion(self, cantidad_marcas):
        ''' Inicia la barra de progreso al exportar pistas de audio separadas. '''
        self.barra_progreso = wx.ProgressDialog(_('Exportando pistas'), _('Espere un momento...'), cantidad_marcas, style=wx.PD_CAN_ABORT | wx.PD_AUTO_HIDE)

    def actualizar_progreso_exportacion(self, progreso, cantidad_marcas):
        ''' Actualiza la barra de progreso. '''
        if self.barra_progreso:
            self.barra_progreso.Update(progreso)
            if self.barra_progreso.WasCancelled():
                self.finalizar_progreso_exportacion()

    def finalizar_progreso_exportacion(self):
        ''' Finaliza la barra de progreso de la exportación. '''
        if self.barra_progreso:
            self.barra_progreso.Destroy()
            self.barra_progreso = None

    def deshacer(self, event):
        self.controlador.deshacer()
        logging.info(_('Se deshacen cambios realizados.'))
        self.lector.output(_('Deshacer'))
        self.refrescar_lista()
        self.controlar_deshacer_reahcer()

    def rehacer(self, event):
        if self.controlador.historial.es_vacia()[1] is False:
            self.controlador.rehacer()
            logging.info(_('Se recuperan cambios deshechos'))
            self.refrescar_lista()
            self.lector.output(_('Rehacer'))
        self.controlar_deshacer_reahcer()

    def controlar_deshacer_reahcer(self):
        ''' controla si deshacer y rehacer se habilitan o ddesabilitan '''
        if self.controlador.historial.es_vacia()[0]:
            self.mn_deshacer.Enable(False)
        else:
            self.mn_deshacer.Enable(True)
        if self.controlador.historial.es_vacia()[1]:
            self.mn_rehacer.Enable(False)
        else:
            self.mn_rehacer.Enable(True)

    def informar_medios(self, event):
        self.vn_informacion = Informacion_medios(None, _('Información de medios'), self.controlador)
        if self.vn_informacion.ShowModal() == wx.OK:
            self.vn_informacion.close()


class Contextual(wx.Menu):
    def __init__(self, parent):
        super(Contextual, self).__init__()
        self.parent = parent
        self.m1 = wx.MenuItem(self, wx.NewId(), _('&Editar') + '\tCtrl+E')
        self.Append(self.m1)
        self.Bind(wx.EVT_MENU, self.abrir_editar2, self.m1)
        self.m2 = wx.MenuItem(self, -1, _('E&liminar'))
        self.Append(self.m2)
        self.Bind(wx.EVT_MENU, self.borrar_item, self.m2)

    def abrir_editar2(self, event):
        self.parent.editar_marca(None)

    def borrar_item(self, event):
        self.parent.borrar_item(None)
