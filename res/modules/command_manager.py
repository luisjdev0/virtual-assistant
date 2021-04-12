from os.path import isfile
import json

#Clase que asocia los comandos con el CCF
class commands:
    '''
    Clase administradora de comandos.
    '''
    #Carga o crea el archivo de control de comandos JSON
    def load():
        '''
        Carga la información de los comandos guardados.
        '''
        from data.info import DIRS, SYSTEM_LOG
        SYSTEM_LOG.write("Cargando clase commandos")
        if (not isfile(DIRS['commands-data'])):
            open(DIRS['commands-data'], 'w', encoding='utf8').close()
            return {}
        else:
            return json.load(open(DIRS['commands-data'], encoding='utf8'))
    
    def save(data):
        '''
        Guarda/Serializa la información de los comandos.
        '''
        from data.info import DIRS, SYSTEM_LOG
        SYSTEM_LOG.write(f"Ejecutando commands.save({data})")
        with open(DIRS['commands-data'], 'w', encoding='utf8') as jsonFile:
            jsonFile.write(json.dumps(data, ensure_ascii=False))

    #Ejecuta el comando CCF según el key (que debe encontrarse en el control de comandos)
    def execute(key):
        '''
        Ejecuta el comando pasado por parámetro (Si existe).

        @param key: Comando que se ejecutará si existe.
        '''
        from data.info import SYSTEM_LOG, globaldata, BASS_DECODER, GUI_CONTROLLER
        global globaldata

        key = key.lower()
        as_name = globaldata['assistant-data']['name']

        if type(as_name) == str:

            if key == "desactivate" or key == "espera" or key == "silencio":
                globaldata['assistant-data']['listen'] = False
                SYSTEM_LOG.write("Asistente entrando en espera")
                BASS_DECODER.reader.decode_line("SPEAK Entraré en modo espera |GLOBALDATA 1|")
                GUI_CONTROLLER.m_window.setWindowTitle(f"{globaldata['assistant-data']['name']} - En espera")
                return 0
                
            elif key == as_name.lower():
                globaldata['assistant-data']['listen'] = True
                GUI_CONTROLLER.m_window.setWindowTitle(f"{globaldata['assistant-data']['name']} - Asistente Virtual")
                SYSTEM_LOG.write("Asistente saliendo de espera")
                BASS_DECODER.reader.decode_line("SPEAK Estoy activo de nuevo |GLOBALDATA 1|")
                return 0

        if globaldata['assistant-data']['listen']:

            SYSTEM_LOG.write(f"Ejecutando commands.execute({key})")

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
        '''
        Decodifica el comando pasado por parámetro.

        @param key: Comando que decodificará.
        '''
        from data.info import command_data, BASS_DECODER, DIRS, SYSTEM_LOG
        SYSTEM_LOG.write(f"Ejecutando commands.run_command({key})")

        for command_info in command_data:
            if key in command_info['keys']:
                path = DIRS['folders']['CMDS-CUSTOM']+f"/{command_info['Command']}"
                return BASS_DECODER.reader.decode_file(path)

        BASS_DECODER.reader.decode_line("SPEAK No comprendo el comando |GLOBALDATA 1|")

#Clase que comprueba los comandos por defecto del asistente
class default_commands:
    '''
    Comandos del asistente por defecto.
    '''
    #Establece y busca si el comando que se envió hace parte de los predeterminados
    def find_command(key):
        '''
        Comprueba si el comando existe dentro de los comandos por defecto.

        @param key: Comando a comprobar.
        '''
        from data.info import SYSTEM_LOG
        SYSTEM_LOG.write(f"Ejecutando default_commands.find_command({key})")

        commands_keys = {
            "ajustes" : default_commands.settings_panel,
            "agregar comandos" : default_commands.add_command_panel,
            "agregar comando" : default_commands.add_command_panel,
            "editar comando" : default_commands.edit_commands_panel,
            "editar comandos" : default_commands.edit_commands_panel,
            "comandos" : default_commands.edit_commands_panel,
            "administrar comandos" : default_commands.edit_commands_panel,
        }

        if key in commands_keys:
            commands_keys[key]()
            return True
        else:
            return False

    #Abre el panel de ajustes mediante Comando por defecto.
    def settings_panel():
        '''
        Abre el panel de ajustes mediante Comando por defecto.
        '''
        from data.info import GUI_CONTROLLER, SYSTEM_LOG
        SYSTEM_LOG.write("Ejecutando default_commands.settings_panel()")
        GUI_CONTROLLER.get_settings_window(0)
        return ""

    #Abre el panel de creación de comandos mediante Comando por defecto.
    def add_command_panel():
        '''
        Abre el panel de creación de comandos mediante Comando por defecto.
        '''
        from data.info import GUI_CONTROLLER, SYSTEM_LOG
        SYSTEM_LOG.write("Ejecutando default_commands.add_command_panel()")
        GUI_CONTROLLER.get_add_commands_window(0)
        return ""
    
    #Abre el administrador de comandos mediante Comando por defecto.
    def edit_commands_panel():
        '''
        Abre el administrador de comandos mediante Comando por defecto.
        '''
        from data.info import GUI_CONTROLLER, SYSTEM_LOG
        SYSTEM_LOG.write("Ejecutando default_commands.edit_command_panel()")
        GUI_CONTROLLER.get_edit_commands_window(0)

