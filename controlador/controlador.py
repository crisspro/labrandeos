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
		self.nombre_app= 'CUE Genesis'
		self.autor_app= 'Crisspro'
		self.licencia_app= 'GPL-3.0'
		self.version_app= 'v1.1'

		self.data  = None
		self.disco = Disco()
		self.tiempo = Tiempo()
		self.ruta_proyecto = 'temp.proyecto.cgp'
		self.actualizado = True


	def verificarNuevaVersion(self):
		try:
			link= 'https://api.github.com/repos/crisspro/keyzoneclassic-ahk/releases/latest'
			coneccion= requests.get(link, timeout= 5)
		except(requests.ConectionError, requests.Timeout):
			print('No hay conección')
		else:
			try:
				v= coneccion.json() ['tag_name']
			except KeyError:
				print('No se ha podido establecer la conexión', 'Error.')
			if v != self.version_app:
				self.actualizado = False
				wx.adv.Sound.PlaySound(os.path.join('vista', 'sounds', 'nueva_version.wav'))
				resp= wx.MessageBox('Hay disponible una nueva versión de ' + self.nombre_app + '(' + v + ')' + '. ¿Quieres descargarla ahora?', caption= 'Aviso', style= wx.YES_NO)
				if resp == wx.YES:
					dw= coneccion.json() ['assets']
					for i in dw:
						dw= i['browser_download_url']
					wx.LaunchDefaultBrowser(dw)
					self.Close()
			else:
				self.actualizado = True

	def crear_disco(self, titulo, autor, genero, ano, comentario):
		self.disco.titulo = titulo
		self.disco.autor = autor
		self.disco.genero = genero
		self.disco.ano = ano
		self.disco.comentario = comentario


	def consultar_autor (self):
		autor = self.disco.autor
		return autor

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
		tiempo =self.tiempo.reconvertir(t)
		return tiempo

	def generar (self):
		if self.in_autor.GetValue() == '' and self.in_album.GetValue() == '':
			nombre_cue= 'Sin autor - Nuevo disco.cue'
			archivo= open( os.path.join(self.dialogo.GetDirectory(), nombre_cue), 'w+')
		elif self.in_autor.GetValue() == '':
			nombre_cue= ('Sin autor - ' + self.in_album.GetValue() + '.cue')
			archivo= open(os.path.join(self.dialogo.GetDirectory(), nombre_cue), 'w+')
		elif self.in_album.GetValue() == '':
			nombre_cue= (self.in_autor.GetValue() + ' - Nuevo disco.cue')
			archivo= open(os.path.join(self.dialogo.GetDirectory(), nombre_cue), 'w+')
		else:
			nombre_cue= (self.in_autor.GetValue() + ' - ' + self.in_album.GetValue() + '.cue')
			archivo= open( os.path.join(self.dialogo.GetDirectory(), nombre_cue), 'w+')
		if self.in_autor.GetValue() != '':
			archivo.write("TITLE "+'"' + self.in_album.GetValue() + '"' + "\n")
		if self.in_album.GetValue() != '':
			archivo.write("PERFORMER " + '"' + self.in_autor.GetValue() + '"' + "\n")
		if self.in_fecha.GetValue() != '':
			archivo.write("REM DATE " + str (self.in_fecha.GetValue()) + "\n")
		if self.in_genero.GetValue() != '':
			archivo.write("REM GENRE " + '"' + self.in_genero.GetValue() + '"' + "\n")
		if self.in_comentarios.GetValue() != '':
			archivo.write("REM COMMENT 		" + '"' + self.in_comentarios.GetValue() + '"' + "\n")
		archivo.write("FILE " + '"' +self.dialogo.GetFilename() + '"' + " ")
		archivo.close()
		if os.path.isfile(os.path.join(self.dialogo.GetDirectory(), nombre_cue)):
			wx.adv.Sound.PlaySound(os.path.join('files', 'sounds', 'ok.wav'))
			resp= wx.MessageBox('El archivo "CUE" ha sido guardado con éxito. ¿Deseas abrir la carpeta de destino?', caption= 'Listo', style= wx.YES_NO)
			if resp == wx.YES:
				os.startfile(self.dialogo.GetDirectory())
		else:
			wx.MessageBox('Ha ocurrido un error. No se ha podido guardar el archivo CUE.', caption= 'Mensaje', style= wx.ICON_ERROR)

	def consultar_datos(self, id):
		marca = self.data.getMarcas()
		return marca(id)


# Creación de instancias

configparser = configparser.ConfigParser()