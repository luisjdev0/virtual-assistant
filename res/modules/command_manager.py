from os.path import isfile
import json

class commands:
    #Carga o crea el archivo de control de comandos
    def load():
        from data.info import DIRS
        if (not isfile(DIRS['commands-data'])):
            cmd_file = open(DIRS['commands-data'], 'w', encoding='utf8')
            cmd_file.close()
            return {}
        else:
            return json.load(open(DIRS['commands-data'], encoding='utf8'))
    #Ejecuta el comando segun ficheros CCF
    def execute(key):
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
    
    def run_command(key):
        from data.info import command_data, BASS_DECODER, DIRS
        for command_info in command_data:
            if key in command_info['keys']:
                path = DIRS['folders']['CMDS-CUSTOM']+f"/{command_info['Command']}"
                return BASS_DECODER.reader.decode_file(path)

        BASS_DECODER.reader.decode_line("SPEAK No comprendo el comando :GLOBALDATA 1:")        