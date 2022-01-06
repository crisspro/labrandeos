import os
import pickle
import requests
import webbrowser
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
			if v != '0.2':
				self.actualizado = False
				wx.adv.Sound.PlaySound(os.path.join('vista', 'sounds', 'nueva_version.wav'))
				resp= wx.MessageBox('Hay disponible una nueva versión de ' + nombre_app + '(' + v + ')' + '. ¿Quieres descargarla ahora?', caption= 'Aviso', style= wx.YES_NO)
				if resp == wx.YES:
					dw= coneccion.json() ['assets']
					for i in dw:
						dw= i['browser_download_url']
					webbrowser.open(dw)
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
		self.save()
		return marca

	def getMarcas(self):
		return self.data.getMarcas()
	
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