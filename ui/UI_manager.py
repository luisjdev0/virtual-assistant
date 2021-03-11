import sys
import time
import threading
from res.modules.command_manager import commands
from PyQt5 import uic
from PyQt5.QtWidgets import QMainWindow, QApplication
from res.modules.voice_controller import speak, recognize

app = QApplication(sys.argv)

#Clase heredable
class window_base(QMainWindow):
    def __init__(self, ui_file):
        super().__init__()
        uic.loadUi(ui_file, self)

#Clase Principal
class main_window(window_base):
    def __init__(self):
        from data.info import APP_VERSION
        super().__init__('ui/main.ui')
        self.AppVersion.setText(APP_VERSION)
        self.SendButton.clicked.connect(self.send_command)
        self.hilo = threading.Thread(target=self.get_voice_data, name="Speech-TT")
        self.hilo2 = threading.Thread(target=self.get_voice_status, name="Speech-TT-STATUS")
        self.hilo2_wait = False
        self.hilo.setDaemon(True);self.hilo2.setDaemon(True)
        self.hilo.start() ; self.hilo2.start()

    #Hilo para escuchar al usuario
    def get_voice_data(self):

        while True:

            text = recognize()
            self.hilo2_wait = True
            self.CommandSpeech.setText(text)
            commands.execute(text)
            time.sleep(3)
            self.hilo2_wait = False

    def get_voice_status(self):
        text = "Escuchando"
        while True:

            if not self.hilo2_wait:
                if text == "Escuchando...":
                    text = "Escuchando"
                else:
                    text += "."

                self.CommandSpeech.setText(text)
            time.sleep(1)
            
    
    def keyPressEvent(self, event):
        from PyQt5 import Qt
        if event.key() == 16777220:
            self.SendButton.click()
    def closeEvent(self, event):
        from data.info import globaldata
        speak(f"Hasta pronto {globaldata['assistant-data']['user-alias']}")

    def send_command(self):

        command = self.CommandInput.text()
        if command == "salir" or command == "exit":
            self.close()
        elif command != "":
            commands.execute(command)


#Clase Ajustes
class settings_window(window_base):
    def __init__(self):
        super().__init__('ui/settings.ui')
        self.SendButton.clicked.connect(self.send_info)
        
        #Definir contenido del combobox
        self.voices = self.get_available_voices()

        for voice in list(self.voices.keys()):
            self.VoiceSelected.addItem(voice)

        self.VoiceSelected.currentIndexChanged.connect(self.check_voice)
        self.VoiceVolume.sliderReleased.connect(self.check_voice)
        self.VoiceRate.sliderReleased.connect(self.check_voice)
    
    def closeEvent(self, event):
        from os.path import isfile
        from data.info import DIRS
        if not isfile(DIRS['user-data']):
            speak("De acuerdo, configuraremos luego")
            sys.exit(0)

    def send_info(self):
        voice_info = self.voices[self.VoiceSelected.currentText()]
        if not self.AssistantName.text() != "" or not self.UserName.text() != "":
            self.StatusLabel.setText("Por favor, rellena todos los campos")
        else:
            if voice_info == -1:
                self.StatusLabel.setText("Por favor elige una voz para mí")
            else:
                from data.info import globaldata, DIRS
                import json

                self.StatusLabel.setText("Guardando información...")

                globaldata['assistant-data']['name'] = self.AssistantName.text()
                globaldata['assistant-data']['user-alias'] = self.UserName.text()
                globaldata['assistant-data']['voice-id'] = voice_info
                globaldata['assistant-data']['voice-volume'] = self.VoiceVolume.value()/100
                globaldata['assistant-data']['voice-rate'] = self.VoiceRate.value()

                try:

                    jsonFile = open(DIRS['user-data'], 'w', encoding='utf8')
                    jsonFile.write(json.dumps(globaldata, ensure_ascii=False))
                    jsonFile.close()
                    self.StatusLabel.setText("Se guardó correctamente")
                    self.close()

                except:

                    self.StatusLabel.setText("No se pudo guardar la información")

            

    #Obtener voices disponibles
    def get_available_voices(self):

        import pyttsx3

        engine = pyttsx3.init()
        voices = engine.getProperty('voices')
        del engine

        available_voices = {
            "Selecciona una voz" : -1,
        }
        
        for voice in voices:
            available_voices[voice.name] = voice.id

        return available_voices

    #Chequear la voz seleccionada
    def check_voice(self):
        import pyttsx3
        engine = pyttsx3.init()
        voice_value = self.voices[self.VoiceSelected.currentText()]
        if voice_value != -1:
            self.StatusLabel.setText(f"Vol {self.VoiceVolume.value()} Rat {self.VoiceRate.value()}")
            engine.setProperty('voice', voice_value)
            engine.setProperty('volume', (self.VoiceVolume.value()/100))
            engine.setProperty('rate', self.VoiceRate.value())
            engine.say("Así suena la voz seleccionada")
            engine.runAndWait()