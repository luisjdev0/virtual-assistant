from res.modules.jls_base import jl_reader

#Clase Base de decodificadores CCF en CASIOPEA
class jls_bass:
	'''
	Carga las utilidades necesarias para decodificar CCF.
	'''
	def __init__(self, keys = ""):
		'''
		Inicia el control del decodificador CCF.

		@param keys: Llaves para cargar las funciones del decodificador CCF.
		'''
		self.control_var = None #Variable de control que registra las últimas entradas
		self.data = {} #Diccionario serializable

		if keys == "":
			self.fkeys = {} #Claves mayores (Funciones principales)
			self.lkeys = {} #Claves menores (Obtienen valores solicitados de funciones o diccionarios)
			self.skeys = {} #Claves decoradoras (Obtienen un valor simple o constante)

		else:
			self.fkeys = keys['fkeys']
			self.lkeys = keys['lkeys']
			self.skeys = keys['skeys']

		#Invoca a la API jls_base
		self.reader = jl_reader(self.fkeys, self.lkeys, self.skeys, thr_exc = False)
