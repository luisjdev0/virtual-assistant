from MODULES.SD import jl_reader

class jls_bass:
	def __init__(self):
		self.control_var = None
		self.data = {}

		self.fkeys = {}
		self.lkeys = {}
		self.skeys = {}
		self.reader = jl_reader(self.fkeys, self.lkeys, self.skeys, thr_exc = True)

class load_jls_info(jls_bass):
	def __init__(self):
		super().__init__()
		self.fkeys = {
			"SPEAK" : lambda x: print(x),
			"LISTEN" : lambda x: self.__listen(x, 0),
			"LISTEN_INT" : lambda x: self.__listen(x, 1),
			"SET" : lambda x: self.__set(x)
		}
		self.lkeys = {
			"DATA" : lambda x: self.data[x[0]]
		}
		self.skeys = {
			"BR" : "\n"
		}

		self.reader = jl_reader(self.fkeys, self.lkeys, self.skeys, thr_exc = True)

	def __listen(self, x, type):

		if type == 1:
			self.control_var = int(input(x))
		else:
			self.control_var = input(x)

		return self.control_var

	def __set(self, x):

		x = x.replace(' ', '')

		if self.control_var != None:
			self.data[x] = self.control_var

			self.control_var = None
		else:
			raise(ValueError("El valor a guardar no puede ser 'None'"))

		return self.data[x]
