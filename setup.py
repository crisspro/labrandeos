import shutil
import os

from cx_Freeze import setup, Executable

# Nombre de la aplicación
app_name = "Labrandeos"
# Nombre del ejecutable
exe_name = "Labrandeos"
# Versión de la aplicación
version = "1.0"
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
    options={"build_exe": {'include_files': includes, "excludes": excludes}},
    executables=[exe]
)


# postcompilación

# Crear una carpeta llamada "accessible_output2" en la carpeta de la compilación
os.makedirs(os.path.join('build', 'accessible_output2'))

# Mover la carpeta que está en la ruta "lib\accessible_output2\lib" dentro de la carpeta de compilación, hacia la carpeta "accessible_output2" creada anteriormente
shutil.move(os.path.join('build', 'lib', 'accessible_output2', 'lib'), os.path.join('build', 'accessible_output2'))

# Eliminar los  archivos .po de las traducciones 
os.remove(os.path.join('build', 'locale', 'en', 'LC_MESSAGES', 'labrandeos.po'))
os.remove(os.path.join('build', 'locale', 'es', 'LC_MESSAGES', 'labrandeos.po'))

# Eliminar el archivo llamado "frozen_application_license.txt" dentro de la carpeta de compilación
os.remove(os.path.join('build', 'frozen_application_license.txt'))
