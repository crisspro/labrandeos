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

# Configuración de las opciones para compilar en MSI

bdist_msi_options = {
	"upgrade_code": "{e46a8049-e897-4b86-bf5f-d6e251596200}",
	"add_to_path": False,
	'all_users': True,
	"initial_target_dir": r"[ProgramFilesFolder]\Labrandeos",
	"data": {
	"Shortcut": [
	(app_name,
'c:\\'	)
	{"name": app_name, "icon": os.path.join('files', 'labrandeos.ico')}]}
}

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
	options={"build_exe": {'include_files': includes, "excludes": excludes}, 'bdist_msi': bdist_msi_options},
	executables=[exe]
)


# postcompilación

# Crear una carpeta llamada "accessible_output2" en la carpeta de la compilación
os.makedirs(os.path.join(base_dir, 'accessible_output2'))

# Mover la carpeta que está en la ruta "lib\accessible_output2\lib" dentro de la carpeta de compilación, hacia la carpeta "accessible_output2" creada anteriormente
shutil.move(os.path.join(base_dir, 'lib', 'accessible_output2', 'lib'), os.path.join(base_dir, 'accessible_output2'))

# Eliminar los  archivos .po de las traducciones 
os.remove(os.path.join(base_dir, 'locale', 'en', 'LC_MESSAGES', 'labrandeos.po'))
os.remove(os.path.join(base_dir, 'locale', 'es', 'LC_MESSAGES', 'labrandeos.po'))

# Eliminar el archivo llamado user.ini dentro de la carpeta "files" 
os.remove(os.path.join(base_dir, 'files', 'user.ini'))

# Eliminar el archivo llamado "frozen_application_license.txt" dentro de la carpeta de compilación
os.remove(os.path.join(base_dir, 'frozen_application_license.txt'))
