import threading

class system_log:
    '''
    Clase para definir el log del sistema
    '''
    def __init__(self, log_print):
        '''
        Inicia el log del sistema.

        @param log_print: True: Se guarda el log, False: No se guarda el log.
        '''
        from datetime import datetime
        self.time = datetime.now()
        self.logfilename = ""
        self.logfilepath = ""
        self.log_print = log_print
        #self.log_file = None
    
    def init(self):
        '''
        Iniciar los recursos del sistema de log.
        '''
        from os.path import isdir
        from os import mkdir
        from data.info import DIRS

        if not isdir(DIRS['folders']['log']):
            mkdir(DIRS['folders']['log'])

        self.logfilename = "%s-%s-%s.log" % (self.time.day, self.time.month, self.time.year)
        self.logfilepath = f"{DIRS['folders']['log']}/{self.logfilename}"
        if self.open_log_file():
            self.log_file.write("\n ---------------------------------- \n\n")

    def write(self, text):
        '''
        Escribir en el log.

        @param text: Texto que se guardará en el log.
        '''
        from datetime import datetime
        try:
            self.open_log_file()
        except:
            print("No se pudo abrir el log file")

        self.time = datetime.now()
        minutes = self.time.minute; seconds = self.time.second
        if self.time.minute < 10:
            minutes = f"0{self.time.minute}"
        if self.time.second < 10:
            seconds = f"0{self.time.second}"

        if self.log_print:
            thread_name = threading.current_thread().name
            _text = "[%s:%s:%s in %s]" % (self.time.hour, minutes, seconds, thread_name)
            self.log_file.write(f"{_text} {text}\n")
            self.log_file.close()

    def open_log_file(self):
        '''
        Abrir el log del asistente del día en curso si existe, de lo contrario lo crea.
        '''
        from os.path import isfile
        if self.log_print:
            if not isfile(self.logfilepath):
                self.log_file = open(self.logfilepath, 'w', encoding='utf8')
                return False
            else:
                self.log_file = open(self.logfilepath, 'a', encoding='utf8')
                return True