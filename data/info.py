import sys
import os
from PyQt5.QtWidgets import QApplication
from res.modules.voice_controller import speak
from res.modules.command_manager import commands
from res.modules.load_jls import jls_bass
from res.modules.CCF_extra_functions import CCF_extra_functions
from ui.UI_manager import *

#Versión del asistente
APP_VERSION = "v0.0.0.4"

#Directorios clave
DIRS = {
    "user-data" : "res/user-data/data.json",
    "commands-data" : "res/user-data/commands-info.json",
    "CMDS" : "res/cmds",
    "CCF" : {
        "MAIN" : 'res/cmds/base/main.CCF',
        "BASE" : 'res/cmds/base/init.CCF'
    },
    "folders" : {
        "user-data" : "res/user-data",
        "CMDS-BASE" : "res/cmds/base",
        "CMDS-CUSTOM" : "res/cmds/custom",
        "audio" : "res/audio"
    }
}

#Información serializable
globaldata = {
    "assistant-data" : {
        "name" : None,
        "user-alias" : None,
        "voice-id" : None,
        "voice-volume" : 1,
        "voice-rate" : 120
    }
}

#Cargar la información de los comandos
command_data = commands.load()

#Clase que controla la UI con CCF
class gui_controller():

    def __init__(self):
        self.m_window = main_window()
        self.m_window.AppVersion.setText(f"Version: {APP_VERSION}")

    #Mostrar ventana principal
    def get_main_window(self, x):
        self.m_window.setWindowTitle(f"{globaldata['assistant-data']['name']} - Asistente Virtual")
        self.m_window.show()
    
    #Mostrar ventana de ajustes
    def get_settings_window(self, x):
        global app
        speak("Abriendo panel de ajustes")
        self.m_window.settings.show()
        try:
            app.exec_()
        except:
            print("El hilo principal ya se encuentra en ejecución")
    
    def get_add_commands_window(self, x):
        speak("Abriendo panel para agregar comandos")
        name = globaldata['assistant-data']['name']
        self.m_window.add_commands_window.setWindowTitle(f"{name} - Agregar Comando")
        self.m_window.add_commands_window.set_viewer_keys()
        self.m_window.add_commands_window.show()


#Instancia de gui_controller
GUI_CONTROLLER = gui_controller()

#Keys para decodificar CCF
keys = {
    "fkeys" : {
        "SPEAK" : lambda x: speak(x),
        "GET-APP" : GUI_CONTROLLER.get_main_window,
        "ADD-COMMAND" : GUI_CONTROLLER.get_add_commands_window,
        "GET-SETTINGS" : GUI_CONTROLLER.get_settings_window,
        "LOAD-DATA" : CCF_extra_functions.load_data,
        "CMD" : CCF_extra_functions.execute_CMD,
        "EXECUTE" : CCF_extra_functions.execute_program

    },
    "skeys" : {

    },
    "lkeys" : {
        "GLOBALDATA" : lambda x: CCF_extra_functions.get_globaldata_info(x),
        "TIME" : lambda x: CCF_extra_functions.get_date_info(x)
    }
}

#Decodificador base
BASS_DECODER = jls_bass(keys)

#Variable del main_window
M_WINDOW = GUI_CONTROLLER.m_window