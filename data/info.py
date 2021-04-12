import sys
import os
from PyQt5.QtWidgets import QApplication
from res.modules.voice_controller import speak
from res.modules.command_manager import commands
from res.modules.load_jls import jls_bass
from res.modules.CCF_extra_functions import CCF_extra_functions
from res.modules.log_system import system_log
from ui.UI_manager import *

#Versión del asistente
APP_VERSION = "v0.0.0.7"

#True para salvar LOG
LOG_PRINT = True

#LOG del sistema
SYSTEM_LOG = system_log(LOG_PRINT)

#Directorios clave
DIRS = {
    "user-data"       : "res/user-data/data.json",
    "commands-data"   : "res/user-data/commands-info.json",
    "CMDS"            : "res/cmds",
    "CCF"     : {
        "MAIN"        : 'res/cmds/base/main.CCF',
        "BASE"        : 'res/cmds/base/init.CCF'
    },
    "folders" : {
        "user-data"   : "res/user-data",
        "CMDS-BASE"   : "res/cmds/base",
        "CMDS-CUSTOM" : "res/cmds/custom",
        "audio"       : "res/audio",
        "log"         : "res/log/"
    }
}

#Información serializable
globaldata = {
    "assistant-data"   : {
        "name"         : None,
        "user-alias"   : None,
        "voice-id"     : None,
        "voice-volume" : 1,
        "voice-rate"   : 120,
        "listen"       : True
    }
}

SYSTEM_LOG.init()

#Clase que controla la UI con CCF
class gui_controller():
    '''
    Clase que controla la UI con CCF
    '''
    def __init__(self):
        SYSTEM_LOG.write("Iniciando GUI controller")
        self.m_window = main_window()
        self.m_window.AppVersion.setText(f"Version: {APP_VERSION}")
        self.splash = None

    #Mostrar ventana principal
    def get_main_window(self, x):
        '''
        Mostrar ventana principal
        '''
        SYSTEM_LOG.write(f"Ejecutando gui_controller.get_main_window({x})")
        self.m_window.setWindowTitle(f"{globaldata['assistant-data']['name']} - Asistente Virtual")
        self.m_window.show()
        self.splash.close()
    
    #Mostrar ventana de ajustes
    def get_settings_window(self, x):
        '''
        Mostrar ventana de ajustes
        '''
        SYSTEM_LOG.write(f"Ejecutando gui_controller.get_settings_window({x})")
        speak("Abriendo panel de ajustes")

        self.m_window.windows['settings'].show()
        self.splash.close()
        
        if not os.path.isfile(DIRS['user-data']):
            app.exec_()
    
    #Mostrar ventana de creación de comandos
    def get_add_commands_window(self, x):
        '''
        Mostrar ventana de creación de comandos
        '''
        SYSTEM_LOG.write(f"Ejecutando gui_controller.get_add_commands_window({x})")
        speak("Abriendo panel para agregar comandos")
        name = globaldata['assistant-data']['name']

        self.m_window.windows['add_commands'].setWindowTitle(f"{name} - Agregar Comando")
        self.m_window.windows['add_commands'].CommandName.setEnabled(True)
        self.m_window.windows['add_commands'].set_viewer_keys()
        self.m_window.windows['add_commands'].CommandName.clear()
        self.m_window.windows['add_commands'].CommandKeys.clear()
        self.m_window.windows['add_commands'].CommandContent.clear()
        self.m_window.windows['add_commands'].show()
    
    #Mostrar ventana de administración de comandos
    def get_edit_commands_window(self, x):
        '''
        Mostrar ventana de administración de comandos
        '''
        SYSTEM_LOG.write(f"Ejecutando gui_controller.get_edit_commands_window({x})")
        speak("Abriendo panel de administración de comandos")

        name = globaldata['assistant-data']['name']

        self.m_window.windows['edit_commands'].setWindowTitle(f"{name} - Administrador de Comandos")
        self.m_window.windows['edit_commands'].show()

    #Obtener Splash Screen
    def get_splash_screen(self, x):
        '''
        Obtener Splash Screen
        '''
        SYSTEM_LOG.write(f"Ejecutando gui_controller.get_splash_screen({x})")
        from PyQt5.QtWidgets import QSplashScreen
        from PyQt5.QtGui import QPixmap
        from time import sleep
        from threading import Thread


        self.splash = QSplashScreen(QPixmap('splash-screen.png'))
        self.splash.show()
        sleep(int(x))


#Cargar la información de los comandos
command_data = commands.load()

#Instancia de gui_controller
GUI_CONTROLLER = gui_controller()

#Keys para decodificar CCF
keys = {
    "fkeys" : {
        "SPEAK"         : lambda x: speak(x),
        "GET-APP"       : GUI_CONTROLLER.get_main_window,
        "ADD-COMMAND"   : GUI_CONTROLLER.get_add_commands_window,
        "EDIT-COMMAND"  : GUI_CONTROLLER.get_edit_commands_window,
        "GET-SETTINGS"  : GUI_CONTROLLER.get_settings_window,
        "SPLASH-SCREEN" : GUI_CONTROLLER.get_splash_screen,
        "LOAD-DATA"     : CCF_extra_functions.load_data,
        "CMD"           : CCF_extra_functions.execute_CMD,
        "EXECUTE"       : CCF_extra_functions.execute_program

    },
    "skeys" : {

    },
    "lkeys" : {
        "GLOBALDATA" : lambda x: CCF_extra_functions.get_globaldata_info(x),
        "TIME"       : lambda x: CCF_extra_functions.get_date_info(x)
    }
}

#Decodificador base
BASS_DECODER = jls_bass(keys)

#Variable del main_window
M_WINDOW = GUI_CONTROLLER.m_window