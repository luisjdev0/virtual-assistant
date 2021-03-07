import os

class CCF_extra_functions:
    
    def load_data(x):
        from data.info import globaldata, DIRS
        global globaldata
        from json import load
        with open(DIRS['user-data'], encoding='utf8') as jsonFile:
            globaldata['assistant-data'] = load(jsonFile)['assistant-data']
            #print(id(globaldata))

    def set_required_folders():
        from data.info import globaldata, DIRS
        global globaldata
        for path in list(DIRS['folders'].keys()):
            if not os.path.exists(DIRS['folders'][path]):
                os.mkdir(DIRS['folders'][path])
                print(f"{DIRS['folders'][path]} was created.")

    def get_globaldata_info(x):
        from data.info import globaldata, DIRS
        global globaldata
        x = int(x[0])
        if x == 1:
            return globaldata['assistant-data']['user-alias']
        elif x == 2:
            return globaldata['assistant-data']['name']
    
    def get_date_info(x):
        x = x[0].upper()
        days = {0: "Lunes", 1: "Martes", 2: "Miercoles", 3: "Jueves", 4: "Viernes", 5: "Sábado", 6: "Domingo"}
        months = {1: "Enero", 2: "Febrero", 3: "Marzo", 4: "Abril", 5: "Mayo", 6: "Junio", 7: "Julio",
        8: "Agosto", 9: "Septiembre", 10: "Octubre", 11: "Noviembre", 12: "Diciembre"}
        from datetime import datetime
        time = datetime.now()

        if x == "S":return time.second
        elif x == "M":return time.minute
        elif x == "H":return time.hour
        elif x == "D":return time.day
        elif x == "MO":return months[time.month]
        elif x == "Y":return time.year
        elif x == "WD":return days[time.weekday()]
        else: return 0
