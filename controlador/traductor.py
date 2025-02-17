import gettext
import os
import logging
from typing import Callable


class Traductor:
    _instance = None
    _initialized = False
    _current_language = None
    _translation_func = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(Traductor, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        if not Traductor._initialized:
            self._initialize()
            Traductor._initialized = True

    def _initialize(self):
        """Inicializa el traductor con la configuración predeterminada"""
        try:
            from controlador.configuracion import Opciones
            opciones = Opciones()
            self._current_language = opciones.consultar_opciones('str', 'general', 'idioma')
        except Exception as e:
            logging.error(f"Error al cargar configuración de idioma: {e}")
            self._current_language = 'es'  # Idioma por defecto

        self._setup_translation()

    def _setup_translation(self):
        """Configura la traducción para el idioma actual"""
        try:
            locale_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'locale')
            translation = gettext.translation(
                'labrandeos',
                localedir=locale_path,
                languages=[self._current_language],
                fallback=True
            )
            self._translation_func = translation.gettext
        except Exception as e:
            logging.error(f"Error al configurar traducción: {e}")
            self._translation_func = lambda x: x  # Fallback a no traducción

    def change_language(self, language_code: str) -> None:
        """
        Cambia el idioma actual de la traducción
        Args:
            language_code (str): Código del idioma (ejemplo: 'es', 'en')
        """
        if self._current_language != language_code:
            self._current_language = language_code
            self._setup_translation()

    @property
    def current_language(self) -> str:
        """Devuelve el código del idioma actual"""
        return self._current_language

    def gettext(self, text: str) -> str:
        """
        Traduce el texto dado
        Args:
            text (str): Texto a traducir

        Returns:
            str: Texto traducido
        """
        return self._translation_func(text)

    @property
    def _(self) -> Callable[[str], str]:
        """
        Devuelve la función de traducción actual

        Returns:
            Callable[[str], str]: Función de traducción
        """
        return self._translation_func


# Crear una instancia global del traductor
_translator = Traductor()


# Función helper para obtener la función de traducción
def get_translator() -> Callable[[str], str]:
    """
    Obtiene la función de traducción actual

    Returns:
        Callable[[str], str]: Función de traducción
    """
    return _translator._


# Exportar _ como una referencia a la función de traducción
_ = _translator._
