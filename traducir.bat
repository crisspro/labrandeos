REM Script cuya función es extraer las cadenas de texto del código fuente, generando un archivo .pot con las cadenas para una posterior traducción.

@echo off


xgettext -o labrandeos.pot main.py update.py vista\principal.py vista\opciones.py vista\editar.py vista\acerca_de.py vista\disco.py vista\informacion_medios.py controlador\controlador.py controlador\configuracion.py controlador\traductor.py

if %ERRORLEVEL% equ 0 (
    echo archivo .pot generado correctamente.
) else (
    echo Hubo un error al extraer las cadenas de texto.
)

pause