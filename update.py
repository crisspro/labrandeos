import logging
import os
import platform
import psutil
import requests
import wx
import subprocess
import threading

from controlador.traductor import _
from controlador.configuracion import LoggingConfig
LoggingConfig.instalar_logging()


class Update(wx.Dialog):
    def __init__(self, parent, title, mensaje, maximo):
        super().__init__(parent, title=title, size=(300, 150))
        self.Show()
        self.api_app = 'https://api.github.com/repos/crisspro/labrandeos/releases/latest'
        self.arquitectura_app = platform.architecture()[0]
        # Crear elementos de la interfaz
        self.mensaje = wx.StaticText(self, -1, mensaje)
        self.dlg_progreso = wx.Gauge(self, range=maximo)
        self.bt_cancelar = wx.Button(self, -1, _('&Cancelar'))
        self.bt_cancelar.SetFocus()
        self.porcentaje = wx.StaticText(self, -1, '0%')
        # Bindear eventos
        self.Bind(wx.EVT_BUTTON, self.cancelar, self.bt_cancelar)
        self.Bind(wx.EVT_CLOSE, self.cancelar)
        # Layout
        self.sz1 = wx.BoxSizer(wx.VERTICAL)
        self.sz1.Add(self.mensaje, 0, wx.ALL | wx.CENTER, 5)
        self.sz1.Add(self.dlg_progreso, 0, wx.EXPAND | wx.ALL, 10)
        self.sz1.Add(self.porcentaje, 0, wx.CENTER | wx.ALL, 5)
        self.sz1.Add(self.bt_cancelar, 0, wx.ALIGN_CENTER | wx.ALL, 10)
        self.SetSizer(self.sz1)
        self.Layout()
        self.Centre()
        self.cancelado = False
        # Iniciar la descarga en un hilo separado
        threading.Thread(target=self.descargar_version, daemon=True).start()

    def cancelar(self, event):
        self.cancelado = True
        logging.info(_('Descarga cancelada.'))
        self.Destroy()

    def actualizar_progreso(self, porcentaje):
        wx.CallAfter(self.dlg_progreso.SetValue, porcentaje)
        wx.CallAfter(self.porcentaje.SetLabel, f'{porcentaje}%')

    def descargar_version(self):
        ''' Detecta la arquitectura de la versión a descargar. '''
        try:
            conexion = requests.get(self.api_app, timeout=5)
            dw = conexion.json()['assets']
            for i in dw:
                url = i['browser_download_url']
                if ('x64' in url and self.arquitectura_app == '64bit') or \
                   ('x86' in url and self.arquitectura_app == '32bit'):
                    logging.info(f'{_("Descargando Labrandeos para")} {self.arquitectura_app}')
                    self.download_file(url)
                    break
        except Exception as e:
            logging.error(f'{_("Error al descargar:")} {e}')
            wx.CallAfter(wx.MessageBox, f'{_("Error al descargar:")} {e}', _('Error'), wx.OK | wx.ICON_ERROR)
            wx.CallAfter(self.Destroy)

    def download_file(self, url):
        ''' Descarga la última versión de Labrandeos. '''
        try:
            response = requests.get(url, stream=True)
            temp_file_path = os.path.join(os.getenv('TEMP'), url.split('/')[-1])
            total_length = int(response.headers.get('content-length', 0))
            if total_length == 0:
                wx.CallAfter(wx.MessageBox, _('No se pudo determinar el tamaño del archivo'), _('Error'), wx.OK | wx.ICON_ERROR)
                logging.error(_('No se pudo determinar el tamaño del archivo'))
                return
            bytes_downloaded = 0
            with open(temp_file_path, 'wb') as f:
                for data in response.iter_content(chunk_size=4096):
                    if self.cancelado:
                        return
                    bytes_downloaded += len(data)
                    f.write(data)
                    progress = int((bytes_downloaded * 100) // total_length)
                    self.actualizar_progreso(progress)
            if not self.cancelado:
                wx.CallAfter(self.finalizar_descarga, temp_file_path)
                logging.info(_('Completada la descarga de Labrandeos.'))
        except Exception as e:
            wx.CallAfter(wx.MessageBox, f'{_("Error durante la descarga:")} {e}', _('Error'), wx.OK | wx.ICON_ERROR)
            logging.error(f'{_("Error durante la descarga:")} {e}')
            wx.CallAfter(self.Destroy)

    def finalizar_descarga(self, temp_file_path):
        self.Destroy()
        self.show_install_dialog(temp_file_path)

    def show_install_dialog(self, installer_path):
        dlg = DialogoAdvertencia(None)
        if dlg.ShowModal() == wx.ID_OK:
            self.run_installer(installer_path)

    def is_process_running(self, process_name):
        try:
            output = subprocess.check_output('tasklist', universal_newlines=True)
            return process_name in output
        except Exception as e:
            wx.MessageBox(f'{_("Error al verificar el proceso:")} {e}', _('Error'), wx.OK | wx.ICON_ERROR)
            logging.error(f'{_("Error al verificar el proceso:")} {e}')
            return False

    def run_installer(self, installer_path):
        ''' Arranca la instalación de Labrandeos. '''
        subprocess.Popen(installer_path, shell=True)
        logging.info(_('Iniciada la instalación de Labrandeos.'))


class DialogoAdvertencia(wx.Dialog):
    def __init__(self, *args, **kw):
        super(DialogoAdvertencia, self).__init__(*args, **kw)
        self.SetTitle("Advertencia")
        # Crear controles del diálogo
        panel = wx.Panel(self)
        vbox = wx.BoxSizer(wx.VERTICAL)
        mensaje = wx.StaticText(panel, label=_('Para continuar con la instalación, por favor, guarde los cambios que haya realizado en el proyecto. Labrandeos se cerrará si decide continuar con la instalación.'))
        vbox.Add(mensaje, flag=wx.ALL, border=10)
        # Botones
        hbox = wx.BoxSizer(wx.HORIZONTAL)
        btn_continuar = wx.Button(panel, label=_('C&ontinuar con la instalación'))
        btn_cancelar = wx.Button(panel, label=_('&Cancelar'))
        btn_cancelar.SetFocus()
        hbox.Add(btn_continuar, flag=wx.RIGHT, border=10)
        hbox.Add(btn_cancelar)
        vbox.Add(hbox, flag=wx.ALIGN_CENTER | wx.TOP, border=20)

        panel.SetSizer(vbox)

        # Bind de eventos
        btn_continuar.Bind(wx.EVT_BUTTON, self.continuar)
        btn_cancelar.Bind(wx.EVT_BUTTON, self.cancelar)

    def continuar(self, event):
        self.finalizar_proceso()
        self.EndModal(wx.ID_OK)

    def cancelar(self, event):
        self.EndModal(wx.ID_CANCEL)

    def finalizar_proceso(self):
        ''' Función que finalizará el proceso Labrandeos.exe '''
        for process in psutil.process_iter(['name']):
            try:
                if process.info['name'] == 'Labrandeos.exe':
                    logging.info(f'{_("Cerrando el proceso:")} {process.info['name']} (PID: {process.pid})')
                    process.terminate()  # Cierra el proceso
                    process.wait()  # Espera a que el proceso se cierre
                    logging.info(_('Proceso cerrado.'))
                    return True
            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess) as e:
                logging.error(f'{_("Error al intentar acceder al proceso 'Labrandeos.exe':")} {e}')


if __name__ == '__main__':
    app = wx.App()
    update = Update(None, _('Descarga'), _('Descargando Labrandeos...'), maximo=100)
    app.MainLoop()
