#Información necesaria
import sys
from PyQt5.QtWidgets import QApplication
from res.modules.voice_controller import speak
from res.modules.load_jls import jls_bass
from ui.UI_manager import *

APP_VERSION = "v0.0.0.1"

#Directorios clave
DIRS = {
    "user-data" : "res/user-data/data.json",
    "cmds" : "res/cmds",
    "CCF" : {
        "MAIN" : 'res/cmds/base/main.CCF',
        "BASE" : 'res/cmds/base/init.CCF'
    }
}

#Información serializable
globaldata = {
    "assistant-data" : {
        "name" : "Casiopea",
        "user-alias" : "Señor",
        "voice-id" : "id",
        "voice-volume" : 1,
        "voice-rate" : 120
    }
}

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

class CCF_extra_functions:
    def load_data(x):
        global globaldata
        from json import load
        jsonFile = open(DIRS['user-data'])
        globaldata = load(jsonFile)
        jsonFile.close()


#Keys para decodificar
keys = {
    "fkeys" : {
        "SPEAK" : lambda x: speak(x),
        "GET-APP" : gui_controller.get_main_window,
        "GET-SETTINGS" : gui_controller.get_settings_window,
        "LOAD-DATA" : CCF_extra_functions.load_data

    },
    "skeys" : {
        "ALIAS" : globaldata['assistant-data']['user-alias'],
        "NAME" : globaldata['assistant-data']['name'],
    },
    "lkeys" : {

    }
}

#Decodificador base
BASS_DECODER = jls_bass(keys)