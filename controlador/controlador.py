import copy
import os
import pickle

from pydub import AudioSegment
import pymediainfo

from modelo.disco import Disco
from modelo.marca import Data, Marca
from modelo.tiempo import Tiempo
from modelo.pista import Pista
from modelo.historial import Historial
from modelo.reproductor import Reproductor


class Controlador():
    def __init__(self):
        self.pista = None
        self.data = None
        self.disco = Disco()
        self.tiempo = Tiempo()
        self.ruta_proyecto = os.path.join(os.environ['LOCALAPPDATA'], 'Labrandeos', 'temp.proyecto.lap')
        self.historial = Historial()
        self.reproductor = Reproductor()

    def crear_proyecto(self):
        self.data = Data()

    def crear_disco(self, titulo, autor, fecha, genero, comentarios):
        self.historial.apilar(self.disco)
        self.disco = Disco()
        self.disco.titulo = titulo
        self.disco.autor = autor
        self.disco.fecha = fecha
        self.disco.genero = genero
        self.disco.comentarios = comentarios
        return self.disco

    def consultar_disco(self):
        return self.disco

    def crearMarca(self, *args, **kwargs):
        data = copy.deepcopy(self.data)
        self.historial.apilar(data)
        marca = Marca(*args, **kwargs)
        self.data.agregarMarca(marca)
        self.data.ordenar()
        return marca

    def editarMarca(self, *args, **kwargs):
        data = copy.deepcopy(self.data)
        self.historial.apilar(data)
        marca = Marca(*args, **kwargs)
        self.data.editarMarca(marca.id, marca)
        self.data.ordenar()
        return marca

    def getMarcas(self):
        return self.data.getMarcas()

    def borrar_marca(self, id):
        self.historial.apilar(copy.deepcopy(self.data))
        self.data.borrar_marca(id)
        self.data.ordenar()

    def load(self):
        """ carga la información del modelo. """
        try:
            f = open(self.ruta_proyecto, "rb")
            self.data = pickle.load(f)
            self.pista = pickle.load(f)
            self.disco = pickle.load(f)
            self.reproductor = pickle.load(f)
            f.close()
        except FileNotFoundError:
            self.data = Data()
            self.disco = Disco()
            self.pista = None
            self.reproductor = Reproductor()

    def save(self):
        """ guarda la información del modelo """
        f = open(self.ruta_proyecto, 'wb')
        pickle.dump(self.data, f)
        pickle.dump(self.pista, f)
        pickle.dump(self.disco, f)
        pickle.dump(self.reproductor, f)
        f.close()

    def limpiar_proyecto(self):
        self.data.limpiar()
        self.data = None
        self.pista = None
        self.disco.limpiar()
        self.disco = Disco()
        self.historial.limpiar()
        self.historial = Historial()
        self.ruta_proyecto = os.path.join(os.environ['LOCALAPPDATA'], 'Labrandeos', 'temp.proyecto.lap')

    def limpiar_temporal(self):
        if os.path.exists(os.path.join(os.environ['LOCALAPPDATA'], 'Labrandeos', 'temp.proyecto.lap')):
            os.remove(os.path.join(os.environ['LOCALAPPDATA'], 'Labrandeos', 'temp.proyecto.lap'))
        self.ruta_proyecto = os.path.join(os.environ['LOCALAPPDATA'], 'Labrandeos', 'temp.proyecto.lap')
        self.data = None

    def temporizar(self, milesimas):
        self.tiempo.milesimas = milesimas
        self.tiempo.convertir(milesimas)

    def cargar_tiempo(self):
        milesimas = self.tiempo.milesimas
        marcos = self.tiempo.marcos
        segundos = self.tiempo.segundos
        minutos = self.tiempo.minutos
        horas = self.tiempo.horas
        return (horas, minutos, segundos, marcos, milesimas)

    def reconvertir(self, t):
        self.tiempo.horas = t[0]
        self.tiempo.minutos = t[1]
        self.tiempo.segundos = t[2]
        self.tiempo.marcos = t[3]
        milesimas = self.tiempo.reconvertir()
        return milesimas

    def exportar_cue(self, indice):
        tipo = self.pista.extension
        tipo = tipo[1:].upper()
        ruta_cue = os.path.join(self.pista.direccion, f'{self.data.titulo} - {self.data.autor}.cue')
        archivo = open(ruta_cue, 'w', encoding='utf-8')
        archivo.write(f'TITLE "{self.disco.titulo}"\n')
        archivo.write(f'PERFORMER "{self.disco.autor}"\n')
        archivo.write(f'REM GENRE "{self.disco.genero}"\n')
        archivo.write(f'REM DATE "{self.disco.fecha}"\n')
        archivo.write(f'REM COMMENT "{self.disco.comentarios}"\n')
        archivo.write(f'FILE "{self.pista.nombre}{self.pista.extension}" {tipo}\n')
        marca = self.getMarcas()
        for marca in marca:
            archivo.write('TRACK ' + str(marca.id).zfill(2) + ' AUDIO' + '\n')
            if indice:
                archivo.write('TITLE "' + str(marca.id).zfill(2) + ' ' + marca.titulo + '"\n')
            else:
                archivo.write('TITLE "' + marca.titulo + '"\n')
            archivo.write('PERFORMER "' + marca.autor + '"\n')
            archivo.write('INDEX 01 ' + str(marca.filtrar_tiempo_inicio_cue()) + '\n')
        archivo.close()
        return ruta_cue

    def seleccionar_audio_salida(self, carpeta, audio, nombre, formato, opciones, tags):
        ''' Selecciona según el formato, la función de exportasión correspondiente. '''
        if formato == 'automático' and self.pista.extension in ['.flac', '.mp3', '.ogg', '.opus', '.wav']:
            formato = self.pista.extension[1:]
            opciones = {'audio': {'formato': formato, 'taza_bit': str(self.pista.taza_bit), 'modo_taza_bit': self.pista.modo_taza_bit, 'velocidad_muestreo': str(self.pista.velocidad_muestreo)}}
        if formato == 'flac':
            self.exportar_flac(carpeta, audio, nombre, opciones, tags)
        elif formato == 'mp3':
            self.exportar_mp3(carpeta, audio, nombre, opciones, tags)
        elif formato == 'ogg':
            self.exportar_ogg(carpeta, audio, nombre, opciones, tags)
        elif formato == 'opus':
            self.exportar_opus(carpeta, audio, nombre, opciones, tags)
        elif formato == 'wav':
            self.exportar_wav(carpeta, audio, nombre, opciones, tags)

    def dividir_audio(self, opciones):
        ''' Divide la pista en segmentos de audio. '''
        nombre_carpeta = f'{self.data.titulo} - {self.data.autor}'
        ruta_carpeta = os.path.join(self.pista.direccion, nombre_carpeta)
        os.makedirs(ruta_carpeta, exist_ok=True)
        archivo = AudioSegment.from_file(self.pista.ruta)
        marca = self.getMarcas()
        fin = self.pista.duracion
        for marca in reversed(marca):
            segmento = archivo[marca.milesimas:fin]
            fin = marca.milesimas
            nombre = f'{marca.id:02} - {marca.titulo}' if opciones['general']['indice'] is True else marca.titulo
            if opciones['audio']['normalizar'] is True:
                segmento = segmento.normalize(headroom=-1.0)
            if opciones['audio']['silencio'] is True:
                segmento = segmento + segmento.silent(duration=2000)
            tags = {'title': marca.titulo, 'artist': marca.autor, 'album': self.disco.titulo, 'year': self.disco.fecha, 'genre': self.disco.genero, 'comment': self.disco.comentarios, 'track_number': marca.id}
            self.seleccionar_audio_salida(nombre_carpeta, segmento, nombre, opciones['audio']['formato'], opciones, tags)
        return ruta_carpeta

    def exportar_audio_automatico(self, carpeta, audio, nombre, tags):
        ''' Exporta audio dependiendo del formato de origen. '''
        audio.export(os.path.join(self.pista.direccion, carpeta, f'{nombre}.{self.pista.extension}'), format=self.pista.extension, bitrate=self.pista.taza_bit, parameters=['-ar', self.pista.velocidad_muestreo], tags=tags)

    def exportar_flac(self, carpeta, audio, nombre, opciones, tags):
        ''' Exporta audio a formato flac. '''
        compresion = opciones['audio']['taza_bit']
        velocidad_muestreo = opciones['audio']['velocidad_muestreo']
        audio.export(os.path.join(self.pista.direccion, carpeta, f'{nombre}.flac'), format='flac', parameters=['-q:a', compresion, '-ar', velocidad_muestreo], tags=tags)

    def exportar_mp3(self, carpeta, audio, nombre, opciones, tags):
        ''' Exporta audio a formato mp3. '''
        taza_bit = opciones['audio']['taza_bit']
        modo_taza_bit = opciones['audio']['modo_taza_bit']
        velocidad_muestreo = opciones['audio']['velocidad_muestreo']
        if modo_taza_bit == 'vbr':
            audio.export(os.path.join(self.pista.direccion, carpeta, f'{nombre}.mp3'), format='mp3', bitrate=taza_bit, parameters=['-q:a', '0', '-ar', velocidad_muestreo], tags=tags)
        elif modo_taza_bit == 'cbr':
            audio.export(os.path.join(self.pista.direccion, carpeta, f'{nombre}.mp3'), format='mp3', bitrate=taza_bit, parameters=['-ar', velocidad_muestreo], tags=tags)

    def exportar_ogg(self, carpeta, audio, nombre, opciones, tags):
        ''' Exporta audio a formato ogg. '''
        taza_bit = opciones['audio']['taza_bit']
        velocidad_muestreo = opciones['audio']['velocidad_muestreo']
        audio.export(os.path.join(self.pista.direccion, carpeta, f'{nombre}.ogg'), format='ogg', bitrate=taza_bit, parameters=['-ar', velocidad_muestreo], tags=tags)

    def exportar_opus(self, carpeta, audio, nombre, opciones, tags):
        ''' Exporta audio a formato opus. '''
        taza_bit = opciones['audio']['taza_bit']
        velocidad_muestreo = opciones['audio']['velocidad_muestreo']
        audio.export(os.path.join(self.pista.direccion, carpeta, f'{nombre}.opus'), format='opus', bitrate=taza_bit, parameters=['-ar', velocidad_muestreo], tags=tags)

    def exportar_wav(self, carpeta, audio, nombre, opciones, tags):
        ''' Exporta audio a formato wav. '''
        velocidad_muestreo = opciones['audio']['velocidad_muestreo']
        audio.export(os.path.join(self.pista.direccion, carpeta, f'{nombre}.wav'), format='wav', parameters=['-ar', velocidad_muestreo], tags=tags)

    def crear_pista(self, nombre, extension, direccion, ruta, duracion):
        self.pista = Pista(nombre, extension, direccion, ruta, duracion)

    def verificar_exportacion(self):
        return os.path.isfile(os.path.join(self.pista.direccion, self.data.titulo + ' - ' + self.data.autor + '.cue'))

    def consultar_datos(self, id):
        marca = self.data.getMarcas()
        return marca[id]

    def comprobar_medios(self, archivo):
        ''' Comprueba si el archivo cargado es de audio '''
        archivo_info = pymediainfo.MediaInfo.parse(archivo)
        for track in archivo_info.tracks:
            if track.track_type == 'Audio':
                info = track.to_data()
                return 'audio', info
            if track.track_type == 'Video':
                return 'otro'
                break

    def aplicar_informacion_medios(self, archivo):
        ''' agrega información de medios al modelo de la pista '''
        archivo_info = pymediainfo.MediaInfo.parse(archivo)
        for track in archivo_info.tracks:
            info = track.to_data()
            self.pista.taza_bit = info.get('bit_rate')
            self.pista.modo_taza_bit = info.get('bit_rate_mode')
            self.pista.velocidad_muestreo = info.get('sampling_rate')
            self.pista.canales = info.get('channel_s')

    def es_temporal(self):
        return self.ruta_proyecto == os.path.join(os.environ['LOCALAPPDATA'], 'Labrandeos', 'temp.proyecto.lap')

    def comparar_modelo(self, ):
        f = open(self.ruta_proyecto, "rb")
        data = pickle.load(f)
        pista = pickle.load(f)
        disco = pickle.load(f)
        f.close()
        return disco == self.disco and pista == self.pista and data == self.data

    def deshacer(self):
        objeto = self.historial.desapilar()
        if objeto.__class__.__name__ == self.data.__class__.__name__:
            self.historial.reservar(copy.deepcopy(self.data))
            self.data = objeto
        elif objeto.__class__.__name__ == self.disco.__class__.__name__:
            self.historial.reservar(copy.deepcopy(self.disco))
            self.disco = objeto

    def rehacer(self):
        objeto = self.historial.reapilar()
        if objeto.__class__.__name__ == self.data.__class__.__name__:
            self.historial.apilar(copy.deepcopy(self.data), False)
            self.data = objeto
        elif objeto.__class__.__name__ == self.disco.__class__.__name__:
            self.historial.apilar(copy.deepcopy(self.disco), False)
            self.disco = objeto
