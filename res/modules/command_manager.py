from os.path import isfile
import json

#Clase que asocia los comandos con el CCF
class commands:
    
    #Carga o crea el archivo de control de comandos JSON
    def load():
        from data.info import DIRS
        if (not isfile(DIRS['commands-data'])):
            open(DIRS['commands-data'], 'w', encoding='utf8').close()
            return {}
        else:
            return json.load(open(DIRS['commands-data'], encoding='utf8'))
    
    def save(data):
        from data.info import DIRS
        with open(DIRS['commands-data'], 'w', encoding='utf8') as jsonFile:
            jsonFile.write(json.dumps(data, ensure_ascii=False))

    #Ejecuta el comando CCF según el key (que debe encontrarse en el control de comandos)
    def execute(key):

        #Si es un comando que debe ejecutarse en hilo principal
        if not default_commands.find_command(key):
            #Comprueba si existe o no el hilo de comandos para ejecutarlos
            import threading
            thread_name = "hilo_comandos"
            #Comprobar la ejecución del hilo para lanzarlo
            is_execute = False
            for i in threading.enumerate():
                if i.getName() == thread_name:
                    is_execute = True
            
            if not is_execute:
                hilo_comandos = threading.Thread(target=commands.run_command, name=thread_name, args=(key, ))
                hilo_comandos.start()
    
    #Decodifica el comando CCF según la key
    def run_command(key):
        from data.info import command_data, BASS_DECODER, DIRS

        for command_info in command_data:
            if key in command_info['keys']:
                path = DIRS['folders']['CMDS-CUSTOM']+f"/{command_info['Command']}"
                return BASS_DECODER.reader.decode_file(path)

        BASS_DECODER.reader.decode_line("SPEAK No comprendo el comando |GLOBALDATA 1|")

#Clase que comprueba los comandos por defecto del asistente
class default_commands:

    def find_command(key):
        commands_keys = {
            "ajustes" : default_commands.settings_panel,
            "agregar comandos" : default_commands.add_command_panel,
            "agregar comando" : default_commands.add_command_panel
        }

        if key in commands_keys:
            commands_keys[key]()
            return True
        else:
            return False

    def settings_panel():
        from data.info import globaldata, GUI_CONTROLLER
        GUI_CONTROLLER.get_settings_window(0)
        return ""

    def add_command_panel():
        from data.info import globaldata, GUI_CONTROLLER
        GUI_CONTROLLER.get_add_commands_window(0)
        return ""
