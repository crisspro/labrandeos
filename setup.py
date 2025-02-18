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
version = "2.0"
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

# Configuración de los ejecutables
main_exe = Executable(
    script=os.path.join(base_dir, "main.py"),
    base="Win32GUI",
    icon=icon_file,
    copyright=copyright,
    target_name=f'{exe_name}.exe'
)

update_exe = Executable(
    script=os.path.join(base_dir, "update.py"),
    base="Win32GUI",  # o "Console" si prefieres que muestre una consola
    icon=icon_file,
    copyright=copyright,
    target_name='update.exe'
)

# Configuración del setup
setup(
    name=app_name,
    version=version,
    author=author,
    description=description,
    options={"build_exe": {'include_msvcr': True, "excludes": excludes, 'include_files': includes}},
    executables=[main_exe, update_exe]  # Lista con ambos ejecutables
)
