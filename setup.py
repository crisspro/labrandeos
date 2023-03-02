import os

import accessible_output2
from cx_Freeze import setup, Executable

def incluir_accesible_output2():
	origen = os.path.join(accessible_output2.__path__[0], 'lib')
	destino = os.path.join('accessible_output2', 'lib')
	return (origen, destino)

# Nombre de la aplicación
app_name = "Labrandeos"
# Nombre del ejecutable
exe_name = "Labrandeos"
# Versión de la aplicación
version = "1.2"
# Nombre del autor
author = "Crisspro"
# Descripción de la aplicación
description = "Labrandeos"
# copyright
copyright = 'Copyright (c) Crisspro'


# Directorio base del proyecto
base_dir = os.path.abspath(os.path.dirname(__file__))

# Archivos y directorios a excluir de la compilación
excludes = []

# archivos incluídos en la compilación 
includes = [
    os.path.join(base_dir, "locale"),
    os.path.join(base_dir, "files")
    ] 

# Ruta al archivo del icono
icon_file = os.path.join(base_dir, "files", "labrandeos.ico")

# Configuración del ejecutable
exe = Executable(
    script=os.path.join(base_dir, "main.py"),
    base="Win32GUI",
    targetName=exe_name,
    icon=icon_file,
	copyright=copyright
	)

# Configuración del setup
setup(
    name=app_name,
    version=version,
    author=author,
    description=description,
    options={"build_exe": {'include_msvcr': True, "excludes": excludes, 'include_files': includes}},
    executables=[exe]
)


# postcompilación
'''
# Eliminar los  archivos .po de las traducciones 
os.remove(os.path.join('build', 'locale', 'en', 'LC_MESSAGES', 'labrandeos.po'))
os.remove(os.path.join('build', 'locale', 'es', 'LC_MESSAGES', 'labrandeos.po'))

# Eliminar el archivo llamado "frozen_application_license.txt" dentro de la carpeta de compilación
os.remove(os.path.join('build', 'frozen_application_license.txt'))
'''