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
        from data.info import APP_VERSION, SYSTEM_LOG
        SYSTEM_LOG.write("Iniciando main_window")
        super().__init__('ui/main.ui')
        self.SendButton.clicked.connect(self.send_command)
        self.AppVersion.setText(APP_VERSION)
        self.hilo = threading.Thread(target=self.get_voice_data, name="Speech-TT")
        self.hilo2 = threading.Thread(target=self.get_voice_status, name="Speech-TT-STATUS")
        self.hilo2_wait = False
        self.hilo.setDaemon(True);self.hilo2.setDaemon(True)
        self.hilo.start() ; self.hilo2.start()
        self.settings = settings_window()
        self.add_commands_window = add_commands_window()
        self.edit_commands_window = edit_commands_window()

        app.focusChanged.connect(self.focus_info)

    def focus_info(self):
        from data.info import globaldata
        if self.isActiveWindow():
            self.setWindowTitle(f"{globaldata['assistant-data']['name']} - Asistente Virtual")

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
        from data.info import globaldata, SYSTEM_LOG
        SYSTEM_LOG.write("Cerrando ventana principal")
        speak(f"Hasta pronto {globaldata['assistant-data']['user-alias']}")

    #Función que envía el comando para ser procesado y decodificado
    def send_command(self):
        from data.info import SYSTEM_LOG
        SYSTEM_LOG.write("Enviando comando desde main_window")
        command = self.CommandInput.text()
        if command == "salir" or command == "exit":
            self.close()
        elif command != "":
            commands.execute(command)


#Clase Panel de Ajustes
class settings_window(window_base):
    def __init__(self):
        from data.info import SYSTEM_LOG
        SYSTEM_LOG.write("Iniciando settings")
        super().__init__('ui/settings.ui')
        self.SendButton.clicked.connect(self.send_info)
        
        #Definir contenido del combobox
        self.voices = self.get_available_voices()

        for voice in list(self.voices.keys()):
            self.VoiceSelected.addItem(voice)

        self.VoiceVolume.sliderReleased.connect(self.check_voice)
        self.VoiceRate.sliderReleased.connect(self.check_voice)
        self.ClearData.clicked.connect(self.clear_data)

        
    def showEvent(self, event):
        from data.info import DIRS, globaldata, SYSTEM_LOG
        SYSTEM_LOG.write("Mostrando ventana de ajustes")
        from os.path import isfile
        if not isfile(DIRS['user-data']):
            self.ClearData.setEnabled(False)
        else:
            self.ClearData.setEnabled(True)
            self.AssistantName.setText(globaldata['assistant-data']['name'])
            self.UserName.setText(globaldata['assistant-data']['user-alias'])
            self.VoiceVolume.setValue(globaldata['assistant-data']['voice-volume']*100)
            self.VoiceRate.setValue(globaldata['assistant-data']['voice-rate'])

            voice_id = globaldata['assistant-data']['voice-id']
            for i in range(len(self.voices.keys())):
                if self.voices[list(self.voices.keys())[i]] == voice_id:
                    self.VoiceSelected.setCurrentIndex(i)
                    break
        self.VoiceSelected.currentIndexChanged.connect(self.check_voice)
    
    #Si se cierra en la configuración inicial, corta el programa y avisa que se configurará luego
    def closeEvent(self, event):
        from os.path import isfile
        from data.info import DIRS, SYSTEM_LOG
        SYSTEM_LOG.write("Cerrando ventana de ajustes")
        if not isfile(DIRS['user-data']):
            speak("De acuerdo, configuraremos luego")
            sys.exit(0)

    #Guarda/Serializa la información suministrada cuando los campos estén completos
    def send_info(self):
        from data.info import SYSTEM_LOG
        SYSTEM_LOG.write("Guardando información de panel de ajustes")

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
                    speak("Se guardó la información")
                    self.close()

                except:
                    self.StatusLabel.setText("No se pudo guardar la información")

            

    #Funcion para Obtener las voices disponibles instaladas
    def get_available_voices(self):
        from data.info import SYSTEM_LOG
        SYSTEM_LOG.write("Obteniendo voces disponibles para ajustes")

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
        from data.info import SYSTEM_LOG
        SYSTEM_LOG.write("Probando voz")

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

    def clear_data(self):
        from os import remove
        from data.info import DIRS, SYSTEM_LOG
        SYSTEM_LOG.write("Borrando datos de usuario")

        speak("Borrando los datos.")
        remove(DIRS['user-data'])
        speak("Se borraron los datos correctamente")
        sys.exit(0)


#Clase Agregar Comandos
class add_commands_window(window_base):
    def __init__(self):
        from data.info import SYSTEM_LOG
        SYSTEM_LOG.write("Iniciando ventana de crear comandos")
        super().__init__('ui/add_command.ui')
        self.CommandTest.clicked.connect(self.test_command)
        self.CommandSave.clicked.connect(self.save_command)

    def set_viewer_keys(self):
        from data.info import SYSTEM_LOG, keys
        SYSTEM_LOG.write("Escribiendo las keys en el creador de comandos")

        self.CommandFKEYS.clear()
        self.CommandSKEYS.clear()
        self.CommandLKEYS.clear()

        #fkeys
        for key in keys['fkeys'].keys():
            self.CommandFKEYS.addItem(key)
        
        #skeys
        for key in keys['skeys'].keys():
            self.CommandSKEYS.addItem(key)

        #lkeys
        for key in keys['lkeys'].keys():
            self.CommandLKEYS.addItem(f"|{key}|")

    def test_command(self):
        from data.info import BASS_DECODER, SYSTEM_LOG
        SYSTEM_LOG.write("Probando el comando escrito")
        BASS_DECODER.reader.decode_document(self.CommandContent.toPlainText())
    
    def check_keys(self):
        from data.info import command_data, SYSTEM_LOG
        SYSTEM_LOG.write("Verificando las KEYS para que sean únicas")
        keys = self.CommandKeys.toPlainText().lower().split(',')
        previous_keys = []
        for command in command_data:
            for key in command["keys"]:
                previous_keys.append(key)

        for key in keys:
            if key in previous_keys:
                return False

        return True

    def save_command(self):
        from res.modules.command_manager import commands
        from data.info import command_data, DIRS, globaldata, SYSTEM_LOG
        SYSTEM_LOG.write("Guardando comando")

        command_isset = False
        for i in range(len(command_data)):
            if command_data[i]['Command'] == self.CommandName.text():
                command_isset = True
                break

        if self.CommandName.text() == "":
            speak("Por favor, introduce un nombre para el comando")
        elif self.CommandKeys.toPlainText() == "":
            speak("Por favor, introduce las claves para el comando")
        elif not command_isset and not self.check_keys():
            speak("Alguna de las claves para el comando ya ha sido usada")
        elif self.CommandContent.toPlainText() == "":
            speak("No puedes guardar un comando vacío")
        else:
            speak("Guardando el comando")

            command_keys = self.CommandKeys.toPlainText().lower().split(",")
            for i in range(len(command_data)):
                if command_data[i]['Command'] == self.CommandName.text():
                    command_data[i]['keys'] = command_keys
                    break
            
            if not command_isset:
                command_data.append({
                    "Command" : f"{self.CommandName.text()}.CCF",
                    "keys" : command_keys
                })


            try:
                if not command_isset:
                    path = f"{DIRS['folders']['CMDS-CUSTOM']}/{self.CommandName.text()}.CCF"
                else:
                    path = f"{DIRS['folders']['CMDS-CUSTOM']}/{self.CommandName.text()}"

                with open(path, 'w', encoding='utf8') as command_file:
                    command_file.write(self.CommandContent.toPlainText())
                
                commands.save(command_data)

                if not command_isset:
                    speak(f"Se guardó el comando {globaldata['assistant-data']['user-alias']}")
                else:
                    speak(f"Se modificó el comando {globaldata['assistant-data']['user-alias']}")

                self.close()
            except:
                speak("No se pudo guardar el comando")
    
    def get_command_to_edit(self, command):
        from data.info import DIRS, SYSTEM_LOG
        SYSTEM_LOG.write("Obteniendo el comando del administrador para editar")

        path = f"{DIRS['folders']['CMDS-CUSTOM']}/{command['Command']}"
        text = open(path, 'r', encoding='utf8').read()

        self.CommandContent.setPlainText(text)
        
        self.CommandName.setText(command['Command'].replace('.CFF', ''))
        self.CommandName.setEnabled(False)
        
        text = ""
        for key in command['keys']:
            text += f"{key},"
        text = text[:-1]
        self.CommandKeys.setPlainText(text)


#Clase Editar Comandos
class edit_commands_window(window_base):
    
    def __init__(self):
        from data.info import SYSTEM_LOG
        SYSTEM_LOG.write("Iniciando clase administrador de comandos")    
        super().__init__('ui/edit_commands.ui')

        self.w_edit_command = add_commands_window()
        self.selected_command = None

        self.CommandEdit.clicked.connect(self.edit_command)
        self.CommandDelete.clicked.connect(self.delete_command)
        self.CommandCreate.clicked.connect(self.create_command)
        self.CommandSelect.currentIndexChanged.connect(self.get_command_keys)
        self.list_commands()
    
    def get_command_keys(self):
        from data.info import command_data, SYSTEM_LOG
        self.KeyList.clear()
        name = self.CommandSelect.currentText()

        SYSTEM_LOG.write(f"Obteniendo las keys para el comando ({name})")

        for command in command_data:
            if command['Command'] == name:
                self.selected_command = command
                self.KeyList.addItems(command['keys'])
                break

    def list_commands(self):
        from data.info import command_data, SYSTEM_LOG
        SYSTEM_LOG.write("Listando los comandos en el administrador")
        #Listar comandos
        self.CommandSelect.clear()
        self.KeyList.clear()
        for command in command_data:
            self.CommandSelect.addItem(command['Command'])

    def closeEvent(self, event):
        from data.info import globaldata, SYSTEM_LOG
        SYSTEM_LOG.write("Cerrando administrador de comandos")
        name = globaldata['assistant-data']['user-alias']
        speak(f"Cerrando panel de comandos {name}.")
        
    def edit_command(self):
        from data.info import globaldata, SYSTEM_LOG
        SYSTEM_LOG.write(f"Enviando para editar el comando {self.selected_command['Command']}")
        name = globaldata['assistant-data']['name']

        self.w_edit_command.get_command_to_edit(self.selected_command)
        self.w_edit_command.setWindowTitle(f"{name} - Agregar Comando")
        self.w_edit_command.set_viewer_keys()
        self.w_edit_command.show()

    def changeEvent(self, event):
        if event.type() == 99:
            if self.isVisible():
                self.list_commands()
    
    def delete_command(self):
        from data.info import command_data, globaldata, DIRS, SYSTEM_LOG
        SYSTEM_LOG.write(f"Eliminando el comando {self.selected_command['Command']}")
        from res.modules.command_manager import commands
        from os import remove
        user = globaldata['assistant-data']['user-alias']

        try:
            speak(f"Eliminando {self.selected_command['Command']}")
            _dir = f"{DIRS['folders']['CMDS-CUSTOM']}/{self.selected_command['Command']}"

            for i in range(len(command_data)):
                if command_data[i]['Command'] == self.selected_command['Command']:
                    command_data.pop(i)
                    break
                
            remove(_dir)
            commands.save(command_data)
            speak(f"Se eliminó el comando {user}.")

        except:
            speak(f"No se pudo eliminar el comando {user}.")
        
        self.list_commands()

    def create_command(self):
        from data.info import GUI_CONTROLLER, SYSTEM_LOG
        SYSTEM_LOG.write("Abriendo ventana para crear comandos desde el administrador")
        GUI_CONTROLLER.get_add_commands_window(0)