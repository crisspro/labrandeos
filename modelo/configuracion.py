from locale import getdefaultlocale


class Configuracion():
    def __init__(self):
        self.idioma_app = ''
        self.dic_general = {
            'idioma': 'en',
            'indice': True,
            'abrir_carpeta': True,
            'detectar_actualizacion': True,
            'sonido_actualizacion': True,
            'sonido_marca': True,
            'sonido_exportar': True
        }
        self.dic_audio = {
            'formato': 'auto',
            'taza_bit': '',
            'modo_taza_bit': '',
            'velocidad_muestreo': '',
            'canales': 2,
            'normalizar': False,
            'silencio': False
        }
        self.añadir_idioma_defecto()

    def añadir_idioma_defecto(self):
        if getdefaultlocale()[0][:2] == 'es':
            self.dic_general['idioma'] = 'es'
        else:
            self.dic_general['idioma'] = 'en'
