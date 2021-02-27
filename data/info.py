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
        "BASE" : 'res/cmds/base/main.CCF',
        "LOAD_INFO" : 'res/cmds/base/init.CCF'
    }
}

#Información serializable
globaldata = {
    "Asistant-name" : "Casiopea"
}

class gui_controller():
    def get_main_window(x):
        app = QApplication(sys.argv)
        window = main_window()
        window.AppVersion.setText(f"Version: {APP_VERSION}")
        window.show()
        sys.exit(app.exec_())


#Keys para decodificar
keys = {
    "fkeys" : {
        "SPEAK" : lambda x: speak(x),
        "GET-APP" : gui_controller.get_main_window
    },
    "skeys" : {

    },
    "lkeys" : {

    }
}

#Decodificador base
BASS_DECODER = jls_bass(keys)