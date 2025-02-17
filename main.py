# título: Labrandeos
# Copyriht (C) 2021 - 2025 Crisspro <crisspro@hotmail.com>
# lisencia: GPL-3.0

import logging
import sys
import os

import wx

import controlador.configuracion
from controlador.controlador import Controlador
from controlador.traductor import _
from vista.principal import Frame


def main():
    App = wx.App()
    logging.info(_('Inicia el arranque de la aplicación'))

    # Configuraciones iniciales
    controlador_app = controlador.configuracion.App()
    controlador_opciones = controlador.configuracion.Opciones()
    controlador_opciones.chequear_ini()
    controlador_opciones.guardar_idioma()
    logging.info(_('Realizadas las configuraciones de idioma'))

    # Controlador principal
    controlador_controlador = Controlador()
    controlador_controlador.limpiar_temporal()
    logging.info(_('Ejecutada limpieza de archivo temporal de proyecto.'))
    controlador_controlador.save()
    logging.info(_('Guardado nuevo archivo temporal de proyecto.'))

    # Crear frame principal
    frame_principal = Frame(None,
                            title=controlador_app.nombre_app,
                            controlador=controlador_controlador,
                            app=controlador_app,
                            opciones=controlador_opciones)
    logging.info(_('Labrandeos iniciado con éxito.'))

    # Manejo de apertura de archivo
    if len(sys.argv) > 1:
        archivo = sys.argv[1]

        # Verificar que el archivo exista y sea .lap
        if os.path.exists(archivo) and archivo.lower().endswith('.lap'):
            try:
                frame_principal.cargar_proyecto(archivo)
            except Exception as e:
                logging.error(f'{_("Error al abrir el proyecto:")} {e}')
                wx.MessageBox(
                    _('No se pudo abrir el proyecto.'),
                    _('Error'),
                    wx.OK | wx.ICON_ERROR
                )

    App.MainLoop()


main()
