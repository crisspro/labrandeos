# título: Labrandeos
# Copyriht (C) 2021 - 2025 Crisspro <crisspro@hotmail.com>
# lisencia: GPL-3.0

import logging

import wx

import controlador.configuracion
from controlador.controlador import Controlador
from controlador.traductor import Traductor
from vista.principal import Frame


traductor = Traductor()
_ = traductor._
App = wx.App()
logging.info(_('Inicia el arranque de la aplicación'))
controlador_app = controlador.configuracion.App()
controlador_opciones = controlador.configuracion.Opciones()
controlador_opciones.chequear_ini()
controlador_opciones.guardar_idioma()
logging.info(_('Realizadas las configuraciones de idioma'))
controlador_controlador = Controlador()
controlador_controlador.limpiar_temporal()
logging.info(_('Ejecutada limpieza de archivo temporal de proyecto.'))
controlador_controlador.save()
logging.info(_('Guardado nuevo archivo temporal de proyecto.'))
Frame(None, title=controlador_app.nombre_app, controlador=controlador_controlador, app=controlador_app, opciones=controlador_opciones)
logging.info(_('Labrandeos iniciado con éxito.'))

App.MainLoop()
