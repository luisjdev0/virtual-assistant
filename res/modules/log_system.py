class system_log:
    def __init__(self, log_print):

        from datetime import datetime
        self.time = datetime.now()
        self.logfilename = ""
        self.logfilepath = ""
        self.log_print = log_print
        #self.log_file = None
    
    def init(self):
        from os.path import isfile, isdir
        from os import mkdir
        from data.info import DIRS

        if not isdir(DIRS['folders']['log']):
            mkdir(DIRS['folders']['log'])

        self.logfilename = "%s-%s-%s.log" % (self.time.day, self.time.month, self.time.year)
        self.logfilepath = f"{DIRS['folders']['log']}/{self.logfilename}"

        if self.log_print:
            if not isfile(self.logfilepath):
                self.log_file = open(self.logfilepath, 'w', encoding='utf8')
            else:
                self.log_file = open(self.logfilepath, 'a', encoding='utf8')
                self.log_file.write("\n ---------------------------------- \n\n")

    def write(self, text):
        if self.log_print:
            _text = "[%s-%s-%s]" % (self.time.hour, self.time.minute, self.time.second)
            self.log_file.write(f"{_text} {text}\n")