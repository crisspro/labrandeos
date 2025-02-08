# título: Labrandeos
# Copyriht (C) 2021 - 2025 Crisspro <crisspro@hotmail.com>
# lisencia: GPL-3.0

import logging
import os

import wx

import controlador.configuracion
from controlador.traductor import Traductor
from controlador.controlador import Controlador
from vista.principal import Frame


def crear_carpeta():
    ''' crea la carpeta Labrandeos en appdata del usuario'''
    ruta_carpeta = os.path.join(os.environ['LOCALAPPDATA'], 'Labrandeos')
    if os.path.exists(ruta_carpeta) is False:
        os.makedirs(os.path.join(os.environ['LOCALAPPDATA'], 'Labrandeos'))
        logging.info(f'{_("Creada carpeta de configuración en:")} {ruta_carpeta}')


traductor = Traductor()
_ = traductor._
controlador.configuracion.LoggingConfig.instalar_logging()

crear_carpeta()

App = wx.App()
logging.info(_('Inicia el arranque de la aplicación'))
controlador_app = controlador.configuracion.App()
controlador_controlador = Controlador()
controlador_opciones = controlador.configuracion.Opciones()
controlador_opciones.chequear_ini()
logging.info(_('Chequeado archivo de configuración.'))
controlador_opciones.guardar_idioma()
logging.info(_('Realizadas las configuraciones de idioma'))
controlador_controlador.limpiar_temporal()
logging.info(_('Ejecutada limpieza de archivo temporal de proyecto.'))
controlador_controlador.save()
logging.info(_('Guardado nuevo archivo temporal de proyecto.'))
Frame(None, title=controlador_app.nombre_app, controlador=controlador_controlador, app=controlador_app, opciones=controlador_opciones)
logging.info(_('Labrandeos iniciado con éxito.'))

App.MainLoop()
