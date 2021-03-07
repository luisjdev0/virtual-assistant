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
    def execute(key):
        from data.info import command_data, BASS_DECODER, DIRS
        for command_info in command_data:
            if key in command_info['keys']:
                path = DIRS['folders']['CMDS-CUSTOM']+f"/{command_info['Command']}"
                return BASS_DECODER.reader.decode_file(path)

        BASS_DECODER.reader.decode_line("SPEAK No comprendo el comando :GLOBALDATA 1:")
                