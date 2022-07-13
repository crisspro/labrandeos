import configparser
import configparser
import os
import pickle
import requests

import wx
from modelo.disco import Disco
from modelo.marca import *
from modelo.tiempo import Tiempo
 
class Controlador():
	def __init__(self):
		self.data  = None
		self.disco = Disco()
		self.tiempo = Tiempo()
		self.ruta_proyecto = 'temp.proyecto.cgp'
		self.ruta_audio = ''




	def crear_disco(self, titulo, autor, fecha, genero, comentarios):
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
		marca = Marca(*args, **kwargs)
		self.data.agregarMarca(marca)
		self.data.ordenar()
		self.save()
		return marca

	def getMarcas(self):
		return self.data.getMarcas()

	def borrar_marca(self, id):
		self.data.borrar_marca(id)
		self.data.ordenar()

	def load(self):
		""" carga la información del modelo. """
		try:
			f = open(self.ruta_proyecto , "rb")
			self.data = pickle.load(f)
			f.close()
		except FileNotFoundError:
			self.data = Data()

	def save(self):
		""" guarda la información del modelo """
		f = open(self.ruta_proyecto , 'wb')
		pickle.dump(self.data, f)
		pickle.dump(self.disco, f)
		f.close()

	def limpiar_temporal(self):
		if os.path.exists('temp.proyecto.cgp'):
			os.remove('temp.proyecto.cgp')


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
		carpeta = os.path.dirname(self.ruta_audio)
		tipo = os.path.splitext(self.ruta_audio)[1]
		tipo = tipo[1:].upper()
		archivo = open(os.path.join(carpeta,  self.disco.titulo + ' - ' + self.disco.autor + '.cue'), 'w')
		archivo.write('TITLE "' + self.disco.titulo + '"\n')
		archivo.write('PERFORMER "' + self.disco.autor + '"\n')
		archivo.write('REM GENRE "' + self.disco.genero + '"\n')
		archivo.write('REM DATE "' + str(self.disco.fecha) + '"\n')
		archivo.write('REM COMMENT "' + self.disco.comentarios + '"\n')
		archivo.write('FILE "' + os.path.basename(self.ruta_audio) + '" ' + tipo + '\n')
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

	def verificar_exportacion(self):
		carpeta = os.path.dirname(self.ruta_audio)
		existe = os.path.isfile(os.path.join(carpeta,  self.disco.titulo + ' - ' + self.disco.autor + '.cue'))
		return existe

	def consultar_datos(self, id):
		marca = self.data.getMarcas()
		return marca(id)


# Creación de instancias

configparser = configparser.ConfigParser()