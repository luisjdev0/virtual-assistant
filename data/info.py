#Información necesaria
import sys
import os
from PyQt5.QtWidgets import QApplication
from res.modules.voice_controller import speak
from res.modules.command_manager import commands
from res.modules.load_jls import jls_bass
from res.modules.CCF_extra_functions import CCF_extra_functions
from ui.UI_manager import *

APP_VERSION = "v0.0.0.3"

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
command_data = commands.load()

class gui_controller():
    def get_main_window(x):
        window = main_window()
        window.AppVersion.setText(f"Version: {APP_VERSION}")
        window.setWindowTitle(f"{globaldata['assistant-data']['name']} - Asistente Virtual")
        window.show()
        app.exec_()
    
    def get_settings_window(x):
        window = settings_window()
        speak('Abriendo panel de ajustes')
        window.show()
        app.exec_()

#Keys para decodificar
keys = {
    "fkeys" : {
        "SPEAK" : lambda x: speak(x),
        "GET-APP" : gui_controller.get_main_window,
        "GET-SETTINGS" : gui_controller.get_settings_window,
        "LOAD-DATA" : CCF_extra_functions.load_data

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