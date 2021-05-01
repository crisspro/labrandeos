#título: CUE Genesis
#autor: Crisspro
#lisencia: GPL-3.0.


import webbrowser
import wx

from controlador import Controlador 
from vista.grafica import Programa

def verificarNuevaVersion(self):
	try:
		link= 'https://api.github.com/repos/crisspro/cuegenesis/releases/latest'
		coneccion= requests.get(link, timeout= 5)
	except(requests.ConectionError, requests.Timeout):
		print('No hay conección')
	else:
		print('Hay conección')
		v= coneccion.json() ['tag_name']
		if v != version_app:
			wx.adv.Sound.PlaySound(os.path.join('vista', 'sounds', 'nueva_version.wav'))
			resp= wx.MessageBox('Hay disponible una nueva versión de ' + nombre_app + '(' + v + ')' + '. ¿Quieres descargarla ahora?', caption= 'Aviso', style= wx.YES_NO)
			if resp == wx.YES:
				dw= coneccion.json() ['assets']
				for i in dw:
					dw= i['browser_download_url']
				webbrowser.open(dw)
				self.Close()

#verificarNuevaVersion()


App= wx.App()
controlador = Controlador()
controlador.load()
Programa(None, title= 'CUE Genesis', controlador=controlador)
App.MainLoop()