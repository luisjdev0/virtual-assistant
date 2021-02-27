from res.modules.jls_base import jl_reader

#Clase Base de decodificadores CCF
class jls_bass:
	def __init__(self, keys = ""):
		self.control_var = None #Variable de control que registra las últimas entradas
		self.data = {} #Diccionario serializable

		if keys == "":
			self.fkeys = {} #Claves mayores (Funciones principales)
			self.lkeys = {} #Claves menores (Obtienen valores solicitados)
			self.skeys = {} #Claves decoradoras (Modifican un valor por otro definido)

		else:
			self.fkeys = keys['fkeys']
			self.lkeys = keys['lkeys']
			self.skeys = keys['skeys']

		#Invoca a la API
		self.reader = jl_reader(self.fkeys, self.lkeys, self.skeys, thr_exc = False)
