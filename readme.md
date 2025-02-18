# Labrandeos

## Índice / Table of Contents

- [Español](#espanol)
- [English](#english)

---

## <a id="espanol" tabindex="-1">Español</a>

**Labrandeos** es un software para dividir y exportar un archivo de audio en múltiples pistas separadas o una única imagen CUE: canciones de un álbum, secciones de un podcast, capítulos de un audiolibro, etc.

## Requisitos del sistema
• Windows 10 o superior, de 32 bits o 64 bits  
• Codecs instalados en tu sistema para los formatos de audio que deseas reproducir.  
• Python 3.12  

## Instrucciones para ejecutar el proyecto

1. Crea un entorno virtual en el que trabajar. Puedes crear uno para 64 bits y otro para 32 bits. Recuerda previamente instalar Python para cada arquitectura.  
2. Activa el entorno virtual que creaste. Por ejemplo, si tu entorno virtual se llama "env":
   ```bash
   .\env\Scripts\activate
   ```

3. Instala todas las bibliotecas necesarias desde "requirements.txt":
   ```bash
   pip install -r requirements.txt
   ```

4. Ejecuta "main.py" desde el directorio raíz del proyecto:
   ```bash
   python main.py
   ```

## Traducciones

Actualmente, labrandeos tiene soporte para los idiomas  Español e inglés, para ello, utiliza la herramienta gettext la cual extrae las cadenas de texto del código fuente, encerradas en _() y exportadas en formato .pot.
Las traducciones se ubican en el directorio "locale" del proyecto. Dentro están las carpetas nombradas con el código según idioma, "es" para español y "en" para inglés.
Cabe señalar que el proyecto está desarrollado nativamente en español, por lo cual las traducciones se deben realizar desde dicho idioma a otro en particular.
Para trabajar las traducciones se deben editar los archivos con extensión .po, los cuales al finalizar los cambios serán compilados en formato .mo.
Es importante que estos archivos siempre mantengan la misma nomenclatura en la ruta. Por ejemplo para traducciones al inglés la ruta debe ser: 
"locale\en\LC_MESSAGES"

Para italiano la ruta debería ser:
"locale\it\LC_MESSAGES"

Solo se debe cambiar el directorio que indica el idioma, el resto de la ruta debe ser siempre la misma. 

* Al compilar el proyecto completo, es importante mantener los archivos .mo, los cuales serán compatibles con el vinario final, por tanto puedes si lo deseas, eliminar los archivos .po al enpaquetar Labrandeos para su distribución.

### Extraer cadenas de texto para su traducción (.pot) con gettext.  

1. Instala gettext en tu equipo. Este software te permitirá extraer las cadenas del código fuente y generar los ficheros (.pot) para trabajar con dichas cadenas. Es importante instalar la versión más actualizada de gettext, ya que se solucionan problemas en la detección de cadenas formateadas con "f" en Python. 
2. En la consola de Windows, asegúrate de estar ubicado en el directorio raíz del proyecto, a continuación genera un archivo con formato .pot mediante el comando "xgettext" mas el nombre del archivo destino e indicando separados por espacio, todos los módulos .py que tengan cadenas de texto encerradas en _(). Aquí un ejemplo breve.   
```bash
xgettext -o labrandeos.pot main.py update.py vista\principal.py
```

Si el comando "xgettext" no es detectado por la consola, asegúrate de que gettext esté habilitado en el path de las variables de entorno de tu sistema. 

* En el proyecto, encontrarás el archivo llamado "traducir.bat" el cual puedes ejecutar desde la consola para generar automáticamente la extracción de cadenas de todos los módulos que las contienen.
```bash
traducir.bat
```

* El resultado al ejecutar el fichero, será el archivo "labrandeos.pot" que se creará en la raíz del proyecto.
* Gettext dispone de otras herramientas que te permitirán generar archivos .po para cada idioma, compilar a .mo, entre otras opciones, no obstante puedes usar el software Poedit para trabajar de forma más sencilla. 

### Traducir cadenas con Poedit

1. instala Poedit en tu equipo.
2. Abre desde Poedit el archivo .pot generado.
3. Presiona el botón "crear traducción nueva", selecciona el idioma al cual quieres traducir el proyecto.
4. Poedit  creará un archivo .po sin guardar aun. Sigue la interfaz del programa y traduce cada cadena de texto que se encuentra en la lista.
5. Guarda los cambios siguiendo la nomenclatura de la ruta como se indicó anteriormente.
6. Poedit guarda el archivo .po y la compilación .mo en el mismo directorio, de no ser así, solo compila como .mo desde Poedit y lo guardas en la ruta ya mencionada.
7. Ahora cuando quieras actualizar tus traducciones, solo edita el archivo .po del idioma correspondiente, actualiza desde el archivo .pot solo si has modificado las cadenas en el código fuente, para finalmente guardar los cambios realizados.
  
## Instrucciones para compilar con cx-Freeze

Para compilar el proyecto en un ejecutable .exe, puedes usar la librería de Python cx-Freeze. 

1. Si utilizaste el archivo "requirements.txt" para instalar las dependencias del proyecto, cx-Freeze ya está instalado en tu entorno, de lo contrario instálalo usando pip.
```bash
pip install cx-freeze
```

2.  Ejecuta el archivo "setup.py":
   ```bash
   python.exe -m setup.py build
   ```

3. Si tienes diferentes entornos para las arquitecturas de 32 bits y 64 bits, realiza el paso anterior en cada entorno para compilar para cada arquitectura.

4. Abre la carpeta "build" en el directorio raíz del proyecto, allí encontrarás el subdirectorio que contiene todos los archivos de la compilación.

## Crear un instalador con Inno Setup

1. Instala Inno Setup en tu equipo.  
2. Abre los archivos "instalador x64.iss" o "instalador x86.iss" desde el compilador de Inno Setup y ejecuta el proceso de compilación.

   * A veces, algunos antivirus detectan el proceso de compilación del instalador como un falso positivo. Si esto ocurre, puedes intentar eliminar las bibliotecas .dll que comienzan con el nombre “api-ms-win-crt-...” ubicadas en el directorio raíz del proyecto compilado con cx-Freeze, ya que podrían ser innecesarias si la computadora en la que se instalará Labrandeos ya las tiene.

## Uso de Labrandeos

1. Carga el archivo de audio que deseas dividir.  
2. Completa los metadatos del álbum.  
3. Reproduce la pista de audio y crea un marcador justo en el punto que deseas.  
4. Una vez que hayas creado todos los marcadores necesarios, elige si deseas exportar como una imagen CUE o como pistas de audio separadas.  
5. Presiona el botón "exportar" para generar el resultado.

   • Al exportar como una imagen CUE, la imagen resultante se guardará en la misma carpeta que el archivo de audio original.  
   • Al elegir pistas de audio separadas, puedes configurar el formato de salida haciendo clic en el botón "opciones".

---

## <a id="english" tabindex="-1">English</a>

**Labrandeos** is a software to split and export an audio file into multiple separate tracks or a unique CUE image: songs from an album, podcast sections, chapters of an audiobook, etc.

## System Requirements
• Windows 10 or higher, 32-bit or 64-bit  
• Codecs installed on your system for the audio formats you want to play.  
• Python 3.12  

## Running Project Instructions

1. Create a virtual environment to work in. You can create one for 64-bit and another for 32-bit. Remember to install Python for the appropriate architecture.  
2. Activate the virtual environment you created. For example, if your virtual environment is called "env":
   ```sh
   .\env\Scripts\activate
   ```

3. Install all necessary libraries from "requirements.txt":
   ```bash
   pip install -r requirements.txt
   ```

4. Run "main.py" from the root project directory:
   ```bash
   python main.py
   ```

## Translations

Currently, labrandeos supports Spanish and English languages. To achieve this, it uses the gettext tool, which extracts the text strings from the source code enclosed in _() and exports them in .pot format.  
The translations are located in the "locale" directory of the project. Inside, there are folders named according to the language code: "es" for Spanish and "en" for English.  
It is important to note that the project is natively developed in Spanish, so translations must be made from this language to another specific one.  
To work on translations, the files with the .po extension must be edited. Once the changes are made, these files will be compiled into .mo format.  
It is important that these files always maintain the same naming convention in the path. For example, for translations to English, the path should be:  
"locale\en\LC_MESSAGES"

For Italian, the path should be:  
"locale\it\LC_MESSAGES"

Only the directory indicating the language should be changed, the rest of the path must always remain the same.

* When compiling the full project, it is important to keep the .mo files, as they will be compatible with the final binary. Therefore, you can, if desired, delete the .po files when packaging Labrandeos for distribution.

### Extracting text strings for translation (.pot) with gettext

1. Install gettext on your computer. This software will allow you to extract the strings from the source code and generate the (.pot) files to work with those strings. It is important to install the latest version of gettext, as issues with detecting strings formatted with "f" in Python are resolved in newer versions.  
2. In the Windows console, make sure you are located in the root directory of the project, then generate a .pot file using the "xgettext" command followed by the target file name and separated by spaces, all the .py modules that contain text strings enclosed in _(). Here's a brief example:  
```bash
xgettext -o labrandeos.pot main.py update.py vista\principal.py
```

If the "xgettext" command is not detected by the console, make sure gettext is enabled in your system's environment variable path.

* In the project, you will find a file called "traducir.bat" which you can run from the console to automatically extract the strings from all the modules that contain them.  
```bash
traducir.bat
```

* The result of running the file will be the "labrandeos.pot" file, which will be created in the root of the project.
* Gettext has other tools that allow you to generate .po files for each language, compile them into .mo files, among other options. However, you can use the Poedit software to work more easily.

### Translating strings with Poedit

1. Install Poedit on your computer.  
2. Open the generated .pot file from Poedit.  
3. Press the "Create new translation" button, and select the language you want to translate the project into.  
4. Poedit will create a .po file without saving it yet. Follow the program's interface and translate each string in the list.  
5. Save the changes, following the naming convention for the path as previously mentioned.  
6. Poedit saves both the .po file and the compiled .mo file in the same directory. If not, just compile the .mo file from Poedit and save it in the path mentioned earlier.  
7. Now, when you want to update your translations, just edit the corresponding .po file, update from the .pot file only if you have modified the strings in the source code, and finally save the changes made.

## Compiling with cx-Freeze

Here is the translated text:

To compile the project into an executable .exe, you can use the Python library cx-Freeze.

1. If you used the "requirements.txt" file to install the project dependencies, cx-Freeze is already installed in your environment. Otherwise, install it using pip.
```bash
pip install cx-freeze
```

2. Run the "setup.py" file:
   ```bash
   python.exe -m setup.py build
   ```

3. If you have different environments for 32-bit and 64-bit architectures, perform the previous step in each environment to compile for each architecture.

4. Open the "build" folder in the project's root directory, there you will find the subdirectory containing all the compiled files.

## Create an Installer with Inno Setup

1. Install Inno Setup on your computer.  
2. Open the "instalador x64.iss" or "instalador x86.iss" files from the Inno Setup compiler and run the compilation process.

   * Sometimes, some antivirus software detects the installer compilation process as a false positive. If this happens, you can try deleting those .dll libraries that start with the name “api-ms-win-crt-...” in the root directory of the project compiled with cx-Freeze, as they could be unnecessary if the computer where Labrandeos will be installed already has them.

## Labrandeos usage

1. Load the audio file you want to split.  
2. Fill in the album metadata.  
3. Play the audio track and create a marker right at the point you want.  
4. Once you have created all the markers you need, choose whether to export as a CUE image or as separate audio tracks.  
5. Press the "export" button to generate the result.

   • When exporting as a CUE image, the resulting image will be saved in the same folder as the original audio.  
   • When choosing separate audio tracks, you can configure the output format by clicking the "options" button.  

