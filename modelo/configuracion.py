from locale import getdefaultlocale

class Configuracion():
	def __init__(self):
		self.idioma_app = ''
		self.dic_general = {'idioma': 'en',
		'cue_id': True,
		'abrir_carpeta': True,
		'sonido_actualizacion': True,
		'sonido_marca': True,
		'sonido_exportar': True}
		self.añadir_idioma_defecto()

	def añadir_idioma_defecto(self):
		if getdefaultlocale()[0][:2] == 'es':
			self.dic_general ['idioma'] = 'es'
		else:
			self.dic_general ['idioma'] = 'en' 