from locale import getdefaultlocale

class Configuracion():
	def __init__(self):
#		<<<<<<< HEAD
		self.dic_general = {'idioma': 'en',
		'cue_id': True,
		'sonido_actualizacion': True,
		'sonido_marca': True,
		'sonido_generar': True}
		self.dic_general ['idioma'] = getdefaultlocale()[0][:2]

