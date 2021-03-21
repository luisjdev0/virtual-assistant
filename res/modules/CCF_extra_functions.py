import os

#Clase estática que controla el comportamiento del CCF
class CCF_extra_functions:
    
    #Carga la información necesaria de los comandos
    def load_data(x):
        from data.info import globaldata, DIRS, SYSTEM_LOG
        SYSTEM_LOG.write(f"Ejecutando CCF_extra_functions.load_data({x})")
        global globaldata
        from json import load
        with open(DIRS['user-data'], encoding='utf8') as jsonFile:
            globaldata['assistant-data'] = load(jsonFile)['assistant-data']

    #Crea los folders necesarios en caso que falten (si es primera ejecución del programa)
    def set_required_folders(x):
        from data.info import globaldata, DIRS, SYSTEM_LOG
        SYSTEM_LOG.write(f"Ejecutando CCF_extra_functions.set_required_folders({x})")
        global globaldata
        for path in list(DIRS['folders'].keys()):
            if not os.path.exists(DIRS['folders'][path]):
                os.mkdir(DIRS['folders'][path])
                print(f"{DIRS['folders'][path]} was created.")

    #Obtiene información de globaldata para los comandos CCF (ej. :GLOBALDATA 1:)
    def get_globaldata_info(x):
        from data.info import globaldata, DIRS, SYSTEM_LOG
        SYSTEM_LOG.write(f"Ejecutando CCF_extra_functions.get_globaldata_info({x})")
        global globaldata
        x = int(x[0])
        if x == 1:
            return globaldata['assistant-data']['user-alias']
        elif x == 2:
            return globaldata['assistant-data']['name']
    
    #Obtiene información de la fecha para los comandos CCF (ej. :TIME S:)
    def get_date_info(x):
        from data.info import SYSTEM_LOG
        SYSTEM_LOG.write(f"Ejecutando CCF_extra_functions.get_date_info({x})")
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

    #Ejecuta en CMD la sentencia escrita con CCF
    def execute_CMD(x):
        from data.info import SYSTEM_LOG
        SYSTEM_LOG.write(f"Ejecutando CCF_extra_functions.execute_CMD({x})")
        os.system(x)
    
    #Ejecuta el programa o la web especificado con CCF
    def execute_program(x):
        from data.info import SYSTEM_LOG
        SYSTEM_LOG.write(f"Ejecutando CCF_extra_functions.execute_program({x})")
        import webbrowser
        webbrowser.open(x)