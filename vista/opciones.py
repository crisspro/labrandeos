import wx

import controlador.configuracion


class Opciones(wx.Dialog):
    def __init__(self, parent, title, opciones):
        super().__init__(parent, title=title)
        self.Center()
        self.controlador_app = controlador.configuracion.App()
        self.controlador_opciones = opciones
        self.Show()

        self.libreta = wx.Notebook(self)
        self.pagina1 = General(self.libreta, self.controlador_opciones)
        self.pagina2 = Audio(self.libreta, self.controlador_opciones)
        self.libreta.AddPage(self.pagina1, _('General'))
        self.libreta.AddPage(self.pagina2, _('Audio'))
        self.botones_dialog = wx.StdDialogButtonSizer()
        self.bt_aceptar = wx.Button(self, wx.ID_OK, _('&Aceptar'))
        self.bt_aceptar.SetDefault()
        self.bt_cancelar = wx.Button(self, wx.ID_CANCEL, _('&Cancelar'))
        self.botones_dialog.AddButton(self.bt_aceptar)
        self.botones_dialog.AddButton(self.bt_cancelar)
        self.botones_dialog.Realize()

        # creación de sizers
        self.sz1 = wx.BoxSizer(wx.VERTICAL)
        self.sz1.Add(self.libreta, 1, wx.EXPAND | wx.ALL, 5)
        self.sz1.Add(self.botones_dialog, 0, wx.ALIGN_RIGHT | wx.ALL, 5)
        self.SetSizerAndFit(self.sz1)


class General(wx.Panel):
    def __init__(self, parent, controlador_opciones):
        wx.Panel.__init__(self, parent)
        self.controlador_opciones = controlador_opciones

        # Creación de controles
#        self = wx.Panel(self)
        self.l_idioma = wx.StaticText(self, -1, _('Idioma'))
        self.lista_idioma = [_('Español'), _('Inglés')]
        self.com_idioma = wx.ComboBox(self, -1, self.completar_idioma(), choices=self.lista_idioma, style=wx.CB_READONLY)
        self.com_idioma.SetFocus()
        self.cas_indice = wx.CheckBox(self, -1, _('Añadir índice al exportar marcas'))
        self.cas_indice.SetValue(self.controlador_opciones.consultar_opciones('bool', 'general', 'indice'))
        self.cas_abrir_carpeta = wx.CheckBox(self, -1, _('Abrir carpeta de destino al exportar'))
        self.cas_abrir_carpeta.SetValue(self.controlador_opciones.consultar_opciones('bool', 'general', 'abrir_carpeta'))
        self.cas_detectar_actualizacion = wx.CheckBox(self, -1, _('Detectar si hay actualizaciones al iniciar'))
        self.cas_detectar_actualizacion.SetValue(self.controlador_opciones.consultar_opciones('bool', 'general', 'detectar_actualizacion'))
        self.cas_sonido_actualizacion = wx.CheckBox(self, -1, _('Sonido al detectar nueva actualización'))
        self.cas_sonido_actualizacion.SetValue(self.controlador_opciones.consultar_opciones('bool', 'general', 'sonido_actualizacion'))
        self.cast_sonido_marca = wx.CheckBox(self, -1, _('Sonido al crear una nueva marca'))
        self.cast_sonido_marca.SetValue(self.controlador_opciones.consultar_opciones('bool', 'general', 'sonido_marca'))
        self.cas_sonido_exportar = wx.CheckBox(self, -1, _('Sonido al exportar el archivo CUE'))
        self.cas_sonido_exportar.SetValue(self.controlador_opciones.consultar_opciones('bool', 'general', 'sonido_exportar'))


# Creación de sizers

        sz1 = wx.BoxSizer(wx.VERTICAL)
        sz1.Add(self.l_idioma)
        sz1.Add(self.com_idioma)
        sz1.Add(self.cas_indice)
        sz1.Add(self.cas_abrir_carpeta)
        sz1.Add(self.cas_sonido_actualizacion)
        sz1.Add(self.cast_sonido_marca)
        sz1.Add(self.cas_sonido_exportar)

        self.SetSizer(sz1)

    def guardar_opciones(self):
        self.controlador_opciones.modelo_configuracion.idioma_app = self.resumir_idioma()
        self.controlador_opciones.guardar_opciones('general', 'indice', str(self.cas_indice.GetValue()))
        self.controlador_opciones.guardar_opciones('general', 'abrir_carpeta', str(self.cas_abrir_carpeta.GetValue()))
        self.controlador_opciones.guardar_opciones('general', 'detectar_actualizacion', str(self.cas_detectar_actualizacion.GetValue()))
        self.controlador_opciones.guardar_opciones('general', 'sonido_actualizacion', str(self.cas_sonido_actualizacion.GetValue()))
        self.controlador_opciones.guardar_opciones('general', 'sonido_marca', str(self.cast_sonido_marca.GetValue()))
        self.controlador_opciones.guardar_opciones('general', 'sonido_exportar', str(self.cas_sonido_exportar.GetValue()))

    def completar_idioma(self):
        prefijo = self.controlador_opciones.consultar_opciones('str', 'general', 'idioma')
        if prefijo == 'es':
            return _('Español')
        elif prefijo == 'en':
            return _('Inglés')

    def resumir_idioma(self):
        idioma = self.com_idioma.GetValue()
        if idioma == _('Español'):
            return 'es'
        elif idioma == _('Inglés'):
            return 'en'


class Audio(wx.Panel):
    def __init__(self, parent, controlador_opciones):
        wx.Panel.__init__(self, parent)
        self.controlador_opciones = controlador_opciones

#        self = wx.Panel(self)
        self.l_formato = wx.StaticText(self, -1, _('Formato:'))
        self.lista_formato = ['automático', 'flac', 'mp3', 'ogg', 'opus', 'wav']
        self.com_formato = wx.ComboBox(self, -1, _('automático'), choices= self.lista_formato, style= wx.CB_READONLY)
        self.Bind(wx.EVT_COMBOBOX, self.habilitar_formato, self.com_formato)
        self.com_formato.SetValue(self.controlador_opciones.consultar_opciones('str', 'audio', 'formato'))
        self.l_taza_bit = wx.StaticText(self, -1, _('Taza de bit:'))
        self.lista_taza_bit = []
        self.com_taza_bit = wx.ComboBox(self, -1, choices=self.lista_taza_bit, style=wx.CB_READONLY)
        self.com_taza_bit.Enable(False)
        self.com_taza_bit.SetValue(self.controlador_opciones.consultar_opciones('str', 'audio', 'taza_bit'))
        self.l_modo_taza_bit = wx.StaticText(self, -1, _('Modo de taza de bit:'))
        self.lista_modo_taza_bit = ['cbr', 'vbr']
        self.com_modo_taza_bit = wx.ComboBox(self, -1, 'cbr', choices= self.lista_modo_taza_bit, style=wx.CB_READONLY)
        self.com_modo_taza_bit.Enable(False)
        self.com_modo_taza_bit.SetValue(self.controlador_opciones.consultar_opciones('str', 'audio', 'modo_taza_bit'))
        self.l_velocidad_muestreo = wx.StaticText(self, -1, _('Velocidad de muestreo:'))
        self.lista_velocidad_muestreo = ['8000', '11025', '16000', '22050', '24000', '32000', '44100', '48000', '88200', '96000', '176400', '192000']
        self.com_velocidad_muestreo = wx.ComboBox(self, -1, '44100', choices=self.lista_velocidad_muestreo, style=wx.CB_READONLY)
        self.com_velocidad_muestreo.Enable(False)
        self.com_velocidad_muestreo.SetValue(self.controlador_opciones.consultar_opciones('str', 'audio', 'velocidad_muestreo'))
        self.cas_normalizar = wx.CheckBox(self, -1, 'Normalizar')
        self.cas_normalizar.SetValue(self.controlador_opciones.consultar_opciones('bool', 'audio', 'normalizar'))
        self.cas_silencio = wx.CheckBox(self, -1, 'Añadir silencio al final de cada pista')
        self.cas_silencio.SetValue(self.controlador_opciones.consultar_opciones('bool', 'audio', 'silencio'))
        self.habilitar_formato(None)

        self.sz1 = wx.BoxSizer(wx.VERTICAL)
        self.sz1.Add(self.l_formato)
        self.sz1.Add(self.com_formato)
        self.sz1.Add(self.l_taza_bit)
        self.sz1.Add(self.com_taza_bit)
        self.sz1.Add(self.l_modo_taza_bit)
        self.sz1.Add(self.com_modo_taza_bit)
        self.sz1.Add(self.l_velocidad_muestreo)
        self.sz1.Add(self.com_velocidad_muestreo)
        self.sz1.Add(self.cas_normalizar)
        self.sz1.Add(self.cas_silencio)
        self.SetSizer(self.sz1)

    def habilitar_formato(self, event):
        ''' habilita controles según formato escogido '''
        formato = self.com_formato.GetValue()
        if formato == _('automático'):
            self.modificar_controles_automatico()
        elif formato == 'opus':
            self.modificar_controles_opus()
        elif formato == 'flac':
            self.modificar_controles_flac()
        elif formato == 'mp3':
            self.modificar_controles_mp3()
        elif formato == 'ogg':
            self.modificar_controles_ogg()
        elif formato == 'wav':
            self.modificar_controles_wav()

    def modificar_controles_automatico(self):
        ''' Modifica los controles mostrados al elegir formato automático. '''
        self.com_modo_taza_bit.Enable(False)
        self.com_taza_bit.Enable(False)
        self.com_velocidad_muestreo.Enable(False)

    def modificar_controles_flac(self):
        ''' Modifica los controles mostrados al elegir el formato flac. '''
        self.com_modo_taza_bit.Enable(False)
        self.l_taza_bit.SetLabel(_('Compresión:'))
        self.lista_taza_bit = [_('0 (más rápido)'), '1', '2', '3', '4', '5', '6', '7', _('8 (más pequeño)')]
        self.com_taza_bit.Enable(True)
        self.com_taza_bit.SetItems(self.lista_taza_bit)
        if self.controlador_opciones.consultar_opciones('str', 'audio', 'taza_bit') in self.lista_taza_bit:
            self.com_taza_bit.SetValue(self.controlador_opciones.consultar_opciones('str', 'audio', 'taza_bit'))
        else:
            self.com_taza_bit.Select(5)
        self.com_velocidad_muestreo.Enable(True)
        self.lista_velocidad_muestreo = ['8000', '11025', '16000', '22050', '24000', '32000', '44100', '48000', '88200', '96000', '176400', '192000']
        self.com_velocidad_muestreo.SetItems(self.lista_velocidad_muestreo)
        if self.controlador_opciones.consultar_opciones('str', 'audio', 'velocidad_muestreo') in self.lista_velocidad_muestreo:
            self.com_velocidad_muestreo.SetValue(self.controlador_opciones.consultar_opciones('str', 'audio', 'velocidad_muestreo'))
        else:
            self.com_velocidad_muestreo.SetValue('48000')

    def modificar_controles_mp3(self):
        ''' Modifica los controles mostrados al elegir el formato mp3. '''
        self.com_modo_taza_bit.Enable(True)
        self.l_taza_bit.SetLabel(_('Taza de bit:'))
        self.lista_taza_bit = ['8 kb/s', '16 kb/s', '24 kb/s', '32 kb/s', '40 kb/s', '48 kb/s', '56 kb/s', '64 kb/s', '80 kb/s', '96 kb/s', '112 kb/s', '128 kb/s', '160 kb/s', '192 kb/s',  '224 kb/s', '256 kb/s', '320 kb/s']
        self.com_taza_bit.Enable(True)
        self.com_taza_bit.SetItems(self.lista_taza_bit)
        if self.controlador_opciones.consultar_opciones('str', 'audio', 'taza_bit') in self.lista_taza_bit:
            self.com_taza_bit.SetValue(self.controlador_opciones.consultar_opciones('str', 'audio', 'taza_bit'))
        else:
            self.com_taza_bit.SetValue('192 kb/s')
        self.com_velocidad_muestreo.Enable(True)
        self.lista_velocidad_muestreo = ['8000', '11025', '12000', '16000', '22050', '24000', '32000', '44100', '48000']
        self.com_velocidad_muestreo.SetItems(self.lista_velocidad_muestreo)
        if self.controlador_opciones.consultar_opciones('str', 'audio', 'velocidad_muestreo') in self.lista_velocidad_muestreo:
            self.com_velocidad_muestreo.SetValue(self.controlador_opciones.consultar_opciones('str', 'audio', 'velocidad_muestreo'))
        else:
            self.com_velocidad_muestreo.SetValue('48000')

    def modificar_controles_ogg(self):
        ''' Modifica los controles mostrados al elegir el formato ogg. '''
        self.com_modo_taza_bit.Enable(False)
        self.l_taza_bit.SetLabel(_('Taza de bit:'))
        self.com_taza_bit.Enable(True)
        self.lista_taza_bit = ['48 kb/s', '56 kb/s', '64 kb/s', '80 kb/s', '96 kb/s', '112 kb/s', '128 kb/s', '160 kb/s', '192 kb/s',  '224 kb/s', '256 kb/s', '320 kb/s']
        self.com_taza_bit.SetItems(self.lista_taza_bit)
        if self.controlador_opciones.consultar_opciones('str', 'audio', 'taza_bit') in self.lista_taza_bit:
            self.com_taza_bit.SetValue(self.controlador_opciones.consultar_opciones('str', 'audio', 'taza_bit'))
        else:
            self.com_taza_bit.SetValue('192 kb/s')
        self.com_velocidad_muestreo.Enable(True)
        self.lista_velocidad_muestreo = ['16000', '22050', '24000', '32000', '44100', '48000']
        self.com_velocidad_muestreo.SetItems(self.lista_velocidad_muestreo)
        if self.controlador_opciones.consultar_opciones('str', 'audio', 'velocidad_muestreo') in self.lista_velocidad_muestreo:
            self.com_velocidad_muestreo.SetValue(self.controlador_opciones.consultar_opciones('str', 'audio', 'velocidad_muestreo'))
        else:
            self.com_velocidad_muestreo.SetValue('48000')

    def modificar_controles_opus(self):
        ''' Modifica los controles mostrados al elegir el formato opus. '''
        self.com_modo_taza_bit.Enable(False)
        self.l_taza_bit.SetLabel(_('Taza de bit:'))
        self.lista_taza_bit = ['8 kb/s', '16 kb/s', '24 kb/s', '32 kb/s', '40 kb/s', '48 kb/s', '56 kb/s', '64 kb/s', '80 kb/s', '96 kb/s', '112 kb/s', '128 kb/s', '160 kb/s', '192 kb/s',  '224 kb/s', '256 kb/s', '320 kb/s']
        self.com_taza_bit.Enable(True)
        self.com_taza_bit.SetItems(self.lista_taza_bit)
        if self.controlador_opciones.consultar_opciones('str', 'audio', 'taza_bit') in self.lista_taza_bit:
            self.com_taza_bit.SetValue(self.controlador_opciones.consultar_opciones('str', 'audio', 'taza_bit'))
        else:
            self.com_taza_bit.SetValue('192 kb/s')
        self.com_velocidad_muestreo.Enable(True)
        self.lista_velocidad_muestreo = ['8000', '12000', '16000', '22050', '24000', '32000', '44100', '48000']
        self.com_velocidad_muestreo.SetItems(self.lista_velocidad_muestreo)
        if self.controlador_opciones.consultar_opciones('str', 'audio', 'velocidad_muestreo') in self.lista_velocidad_muestreo:
            self.com_velocidad_muestreo.SetValue(self.controlador_opciones.consultar_opciones('str', 'audio', 'velocidad_muestreo'))
        else:
            self.com_velocidad_muestreo.SetValue('44100')

    def modificar_controles_wav(self):
        ''' Modifica los controles mostrados al elegir el formato wav. '''
        self.com_modo_taza_bit.Enable(False)
        self.com_taza_bit.Enable(False)
        self.com_velocidad_muestreo.Enable(True)
        self.lista_velocidad_muestreo = ['6000', '8000', '16000', '22050', '24000', '32000', '44100', '48000', '88200', '96000', '176400', '192000']
        self.com_velocidad_muestreo.SetItems(self.lista_velocidad_muestreo)
        if self.controlador_opciones.consultar_opciones('str', 'audio', 'velocidad_muestreo') in self.lista_velocidad_muestreo:
            self.com_velocidad_muestreo.SetValue(self.controlador_opciones.consultar_opciones('str', 'audio', 'velocidad_muestreo'))
        else:
            self.com_velocidad_muestreo.SetValue('48000')

    def guardar_opciones(self):
        ''' Guarda las configuraciones de audio escogidas por el usuario. '''
        self.controlador_opciones.guardar_opciones('audio', 'formato', str(self.com_formato.GetValue()))
        if self.com_formato.GetValue() == 'flac':
            self.controlador_opciones.guardar_opciones('audio', 'taza_bit', str(self.com_taza_bit.GetValue()[0]))
        else:
            self.controlador_opciones.guardar_opciones('audio', 'taza_bit', str(self.com_taza_bit.GetValue()[:-3]))
        self.controlador_opciones.guardar_opciones('audio', 'modo_taza_bit', str(self.com_modo_taza_bit.GetValue()))
        self.controlador_opciones.guardar_opciones('audio', 'velocidad_muestreo', str(self.com_velocidad_muestreo.GetValue()))
        self.controlador_opciones.guardar_opciones('audio', 'normalizar', str(self.cas_normalizar.GetValue()))
        self.controlador_opciones.guardar_opciones('audio', 'silencio', str(self.cas_silencio.GetValue()))
