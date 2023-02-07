import pdb
import copy
import os
import pickle
import requests

import pymediainfo
import wx
from modelo.disco import Disco
from modelo.marca import *
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
		self.ruta_proyecto = 'temp.proyecto.cgp'
		self.historial = Historial()
		self.reproductor = Reproductor()


	def crear_proyecto(self):
		self.data = Data()

	def crear_disco(self, titulo, autor, fecha, genero, comentarios):
		self.historial.apilar('pila1', self.disco)
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
		self.historial.apilar('pila1', data)
		marca = Marca(*args, **kwargs)
		self.data.agregarMarca(marca)
		self.data.ordenar()
		return marca

	def editarMarca(self, *args, **kwargs):
		data = copy.deepcopy(self.data)
		self.historial.apilar('pila1', data)
		marca = Marca(*args, **kwargs)
		self.data.editarMarca(marca.id, marca)
		self.data.ordenar()
		return marca
		
	def getMarcas(self):
		return self.data.getMarcas()

	def borrar_marca(self, id):
		self.historial.apilar('pila1', copy.deepcopy(self.data))
		self.data.borrar_marca(id)
		self.data.ordenar()

	def load(self):
		""" carga la información del modelo. """
		try:
			f = open(self.ruta_proyecto , "rb")
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
		f = open(self.ruta_proyecto , 'wb')
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

	def limpiar_temporal(self):
		if os.path.exists('temp.proyecto.cgp'):
			os.remove('temp.proyecto.cgp')
		self.ruta_proyecto = 'temp.proyecto.cgp'
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
		self.tiempo.minutos= t[1]
		self.tiempo.segundos= t[2]
		self.tiempo.marcos= t[3]
		milesimas = self.tiempo.reconvertir()
		return milesimas

	def generar_cue (self, id):
		tipo = self.pista.extencion
		tipo = tipo[1:].upper()
		archivo = open(os.path.join(self.pista.direccion,  self.disco.titulo + ' - ' + self.disco.autor + '.cue'), 'w')
		archivo.write('TITLE "' + self.disco.titulo + '"\n')
		archivo.write('PERFORMER "' + self.disco.autor + '"\n')
		archivo.write('REM GENRE "' + self.disco.genero + '"\n')
		archivo.write('REM DATE "' + str(self.disco.fecha) + '"\n')
		archivo.write('REM COMMENT "' + self.disco.comentarios + '"\n')
		archivo.write('FILE "' + self.pista.nombre + self.pista.extencion + '" ' + tipo + '\n')
		marca = self.getMarcas()
		for marca in marca:
			archivo.write('TRACK ' + str(marca.id).zfill(2) + ' AUDIO' + '\n')
			if id == True:
				archivo.write('TITLE "' + str(marca.id).zfill(2) + ' ' + marca.titulo + '"\n')
			else:
				archivo.write('TITLE "' + marca.titulo + '"\n')
			archivo.write('PERFORMER "' + marca.autor + '"\n')
			archivo.write('INDEX 01 ' +str(marca.filtrar_tiempo_inicio_cue()) + '\n')
		archivo.close()

	def crear_pista(self, nombre, extencion, direccion, ruta, duracion):
		self.pista = Pista(nombre, extencion, direccion, ruta, duracion)


	def verificar_exportacion(self):
		existe = os.path.isfile(os.path.join(self.pista.direccion,  self.disco.titulo + ' - ' + self.disco.autor + '.cue'))
		return existe

	def consultar_datos(self, id):
		marca = self.data.getMarcas()
		return marca[id]

	def comprobar_medios(self, archivo):
		archivo_info= pymediainfo.MediaInfo.parse(archivo)
		for track in archivo_info.tracks:
			if track.track_type == 'Audio':
				info = track.to_data()
				return 'audio', info
			if track.track_type == 'Video':
				return 'otro'
				break

	def deshacer(self):
		self.historial.apilar('pila2', copy.deepcopy(self.data))
		objeto = self.historial.desapilar('pila1')
		if objeto.__class__.__name__ == self.data.__class__.__name__:
			self.data = objeto
		elif objeto.__class__.__name__ == self.disco.__class__.__name__:
			self.disco = objeto


	def rehacer(self):
		objeto =self.historial.desapilar('pila2')
		if objeto.__class__.__name__ == self.data.__class__.__name__:
			self.data = objeto
		elif objeto.__class__.__name__ == self.disco.__class__.__name__:
			self.disco = objeto
		self.historial.apilar('pila1', copy.deepcopy(self.data))


