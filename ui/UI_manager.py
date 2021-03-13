import sys
import time
import threading
from res.modules.command_manager import commands
from PyQt5 import uic
from PyQt5.QtWidgets import QMainWindow, QApplication
from res.modules.voice_controller import speak, recognize

#Aplicación principal que arranca en "main.py"
app = QApplication(sys.argv)

#Clase base para cargar las UI (para UI files)
class window_base(QMainWindow):
    def __init__(self, ui_file):
        super().__init__()
        uic.loadUi(ui_file, self)

#Clase Ventana Principal
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
        self.settings = settings_window()
        self.add_commands_window = add_commands_window()

    #Hilo para escuchar al usuario
    def get_voice_data(self):

        while True:

            text = recognize()
            self.hilo2_wait = True
            self.CommandSpeech.setText(text)
            commands.execute(text)
            time.sleep(3)
            self.hilo2_wait = False

    #Hilo para mostrar texto "Escuchando..." o lo que dijo el usuario
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
            
    #Envía el comando si se pulsa tecla enter
    def keyPressEvent(self, event):
        from PyQt5 import Qt
        if event.key() == 16777220:
            self.SendButton.click()
    
    #Se despide el asistente si se cierra el programa
    def closeEvent(self, event):
        from data.info import globaldata
        speak(f"Hasta pronto {globaldata['assistant-data']['user-alias']}")

    #Función que envía el comando para ser procesado y decodificado
    def send_command(self):

        command = self.CommandInput.text()
        if command == "salir" or command == "exit":
            self.close()
        elif command != "":
            commands.execute(command)


#Clase Panel de Ajustes
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
    
    #Si se cierra en la configuración inicial, corta el programa y avisa que se configurará luego
    def closeEvent(self, event):
        from os.path import isfile
        from data.info import DIRS
        if not isfile(DIRS['user-data']):
            speak("De acuerdo, configuraremos luego")
            sys.exit(0)

    #Guarda/Serializa la información suministrada cuando los campos estén completos
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

                speak("Guardando la información")

                self.StatusLabel.setText("Guardando información...")

                globaldata['assistant-data']['name'] = self.AssistantName.text()
                globaldata['assistant-data']['user-alias'] = self.UserName.text()
                globaldata['assistant-data']['voice-id'] = voice_info
                globaldata['assistant-data']['voice-volume'] = self.VoiceVolume.value()/100
                globaldata['assistant-data']['voice-rate'] = self.VoiceRate.value()

                try:

                    with open(DIRS['user-data'], 'w', encoding='utf8') as jsonFile:
                        jsonFile.write(json.dumps(globaldata, ensure_ascii=False))

                    self.StatusLabel.setText("Se guardó correctamente")
                    self.close()

                except:
                    self.StatusLabel.setText("No se pudo guardar la información")

            

    #Funcion para Obtener las voices disponibles instaladas
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

    #Función para Chequear la voz seleccionada
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

#Clase Agregar Comandos
class add_commands_window(window_base):
    def __init__(self):
        super().__init__('ui/add_command.ui')
        self.CommandTest.clicked.connect(self.test_command)
        self.CommandSave.clicked.connect(self.save_command)

    def set_viewer_keys(self):
        from data.info import keys

        #fkeys
        text = ""
        for key in keys['fkeys'].keys(): text += f"{key}\n"
        self.CommandFKEYS.setText(text)
        
        #skeys
        text = ""
        for key in keys['skeys'].keys(): text += f"${key}\n"
        self.CommandSKEYS.setText(text)

        #lkeys
        text = ""
        for key in keys['lkeys'].keys(): text += f"|{key}|\n"
        self.CommandLKEYS.setText(text)

    def test_command(self):
        from data.info import BASS_DECODER
        BASS_DECODER.reader.decode_document(self.CommandContent.toPlainText())

    def save_command(self):
        from res.modules.command_manager import commands
        from data.info import command_data, DIRS, globaldata
        if self.CommandName.text() == "":
            speak("Por favor, introduce un nombre para el comando")
        elif self.CommandKeys.toPlainText() == "":
            speak("Por favor, introduce")
        elif self.CommandContent.toPlainText() == "":
            speak("No puedes guardar un comando vacío")
        else:
            speak("Guardando el comando")
            try:
                path = f"{DIRS['folders']['CMDS-CUSTOM']}/{self.CommandName.text()}.CCF"
                with open(path, 'w', encoding='utf8') as command_file:
                    command_file.write(self.CommandContent.toPlainText())
                
                command_keys = self.CommandKeys.toPlainText().split(",")
                command_data.append({
                    "Command" : f"{self.CommandName.text()}.CCF",
                    "keys" : command_keys
                })
                commands.save(command_data)
                speak(f"Se guardó el comando {globaldata['assistant-data']['user-alias']}")
                self.close()
            except:
                speak("No se pudo guardar el comando")
