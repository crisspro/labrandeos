import psutil
from configparser import ConfigParser
import os
import platform
import webbrowser


import requests

import modelo.configuracion


class App():
    def __init__(self):
        self.nombre_app = 'Labrandeos'
        self.autor_app = 'Crisspro'
        self.licencia_app = 'GPL 3.0'
        self.sitio_app = 'https://github.com/crisspro/labrandeos'
        self.api_app = 'https://api.github.com/repos/crisspro/labrandeos/releases/latest'
        self.arquitectura_app = platform.architecture()[0]
        self.version_app = 'v2.0'
        self.actualizado = True

    def verificarNuevaVersion(self):
        try:
            coneccion = requests.get(self.api_app, timeout=5)
        except:
            print('No hay conección')
        else:
            try:
                v = coneccion.json()['tag_name']
                if v != self.version_app:
                    self.actualizado = False
                else:
                    self.actualizado = True
            except KeyError:
                print('No se ha podido establecer la conexión', 'Error.')

    def descargar_version(self):
        coneccion = requests.get(self.api_app, timeout=5)
        dw = coneccion.json()['assets']
        for i in dw:
            dw = i['browser_download_url']
            if 'x64' in dw and self.arquitectura_app == '64bit':
                webbrowser.open(dw)
                break
            elif 'x86' in dw and self.arquitectura_app == '32bit':
                webbrowser.open(dw)
                break

    def verificar_instancia(self):
        ''' Verifica si se está ejecutando otra instancia del programa '''
        proceso = psutil.Process()
        procesos = psutil.process_iter()
        cantidad = 0
        for i in procesos:
            if i.name() == proceso.name() and proceso.name() != 'python.exe':
                cantidad += 1
                if cantidad > 1:
                    return True


class Opciones():
    def __init__(self):
        self.configparser = ConfigParser()
        self.archivo_configuracion = os.path.join(os.environ['LOCALAPPDATA'], 'Labrandeos', 'user.ini')
        self.configparser.read(self.archivo_configuracion, encoding='utf-8')
        self.modelo_configuracion = modelo.configuracion.Configuracion()

    def chequear_ini(self):
        if os.path.isfile(self.archivo_configuracion) is False:
            self.guardar_defecto()
        if set(self.configparser['general']) != set(self.modelo_configuracion.dic_general.keys()):
            self.guardar_defecto()

    def guardar_defecto(self):
        ''' guarda archivo de configuración ini con valores por defecto. '''
        self.configparser['general'] = self.modelo_configuracion.dic_general
        self.configparser['audio'] = self.modelo_configuracion.dic_audio
        archivo = open(self.archivo_configuracion, 'w', encoding='UTF-8')
        self.configparser.write(archivo)
        archivo.close()

    def guardar_idioma(self):
        self.modelo_configuracion.idioma_app = self.consultar_opciones('str', 'general', 'idioma')

    def guardar_opciones(self, seccion, clave, valor):
        self.configparser.set(seccion, clave, str(valor))
        archivo = open(self.archivo_configuracion, 'w', encoding='UTF-8')
        self.configparser.write(archivo)
        archivo.close()

    def convertir_valor(self, valor):
        ''' Convierte a valores python cadenas de texto. '''
        if valor == 'False':
            return False
        elif valor == 'True':
            return True
        elif valor == 'None':
            return None
        else:
            return valor

    def consultar_opciones(self, tipo, seccion, clave):
        self.configparser.read(self.archivo_configuracion, encoding='utf-8')
        if tipo == 'bool':
            return self.configparser.getboolean(seccion, clave)
        elif tipo == 'str':
            return self.configparser.get(seccion, clave)

    def consultar_todas_opciones(self):
        ''' Debuelve un diccionario con todos los valores del .ini. '''
        self.configparser.read(self.archivo_configuracion, encoding='utf-8')
        dic_opciones = {section: dict(self.configparser.items(section)) for section in self.configparser.sections()}
        dic_opciones = {section: {key: self.convertir_valor(value) for key, value in self.configparser.items(section)} for section in self.configparser.sections()}
        return dic_opciones

    def refrescar_ini(self):
        self.configparser = ConfigParser()
        self.archivo_configuracion = os.path.join('files', 'user.ini')
        self.configparser.read(self.archivo_configuracion, encoding='utf-8')
