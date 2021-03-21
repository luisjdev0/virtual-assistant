from sys import exc_info

#Clase base para decodificar CCF
class jl_reader:
	def __init__ (self, fkeys : dict, lkeys : dict, skeys : dict, fsep = '$', lsep = '|', thr_exc = False):

		self.fkeys = fkeys
		self.lkeys = lkeys
		self.skeys = skeys
		self.fsep = fsep
		self.lsep = lsep
		self.thr_exc = thr_exc
	
	#Decodifica las LKEYS de la línea introducida
	def __decode_lkeys(self, line):
		if line.find(self.lsep) == -1:
			return (None, None)
		else:
			word = line[line.find(self.lsep) + 1: line.find(self.lsep, line.find(self.lsep) + 1)]
			line_words = word.split(' ')

			if line_words[0] in self.lkeys:
				value = (str(word), str(self.lkeys[line_words[0]](line_words[1:len(line_words)])))
				return value
			else:
				print(f"No existe una función lista llamada '{line_words[0]}'")
				return (None, None)

	#Separa una lína por los espacios en blanco para ser procesada por los decodificadores
	def __sentence_to_list(self, sentence):
		return sentence.split(' ')

	#Convierte la línea separada de nuevo en una cadena para su procesamiento final
	def __list_to_sentence(self, list_sentence):
		word = ""
		for i in list_sentence:
			word += f"{str(i)} "

		return word

	#Decodifica la línea pasada por parámetro
	def decode_line(self, line):
		
		#Si la línea está vacía, retorna None
		if line.split(' ')[0] == ' ' or line.split(' ')[0] == '':
			return None

		try:
			#Separa la línea para comezar a decodificar en la variable "sentence"
			line_words = line.split(' ')
			sentence = []

			#Decodifica las SKEYS
			for i in range(1, len(line_words)):
				if line_words[i].find(self.fsep) != -1:
					if line_words[i].replace(self.fsep, '') in self.skeys:
						sentence.append(self.skeys[line_words[i].replace(self.fsep, '')])
					else:
						sentence.append(line_words[i])
				else:
					sentence.append(line_words[i])

			#Decodifica las LKEYS
			word = self.__list_to_sentence(sentence)
			while word.find(self.lsep) != -1:
				lkey = self.__decode_lkeys(word)
				if lkey != (None, None):
					word = word.replace(self.lsep+lkey[0]+self.lsep, lkey[1])
			sentence = self.__sentence_to_list(word)
			#Decodifica las FKEYS
			if line_words[0].find(self.lsep) == -1:
				if line_words[0] in self.fkeys:
					return self.fkeys[line_words[0]](self.__list_to_sentence(sentence))
				else:
					print(f"No existe una función llamada '{line_words[0]}'")
		
		#En caso de no lograrlo, lanza una excepción o muestra información según el parámetro "thr_exc"
		except Exception: 
			if not self.thr_exc:
				print(f"Hubo un error: {exc_info()[1]}")
			else:
				raise exc_info()[0](exc_info()[1])
	
	#Decodifica un fichero línea a línea
	def decode_file(self, file_path):
		outputs = []
		with open(file_path, "r", encoding='UTF-8') as file:
			lines = list(file.readlines())

			for i in range(len(lines)):
				lines[i] = lines[i].replace("\n", '')
				outputs.append(self.decode_line(lines[i]))
				
		return outputs
	
	#Decodifica texto plano como si fuera un documento externo
	def decode_document(self, text):
		lines = text.split('\n')
		for i in range(len(lines)):
			lines[i] = lines[i].replace("\n", '')
			self.decode_line(lines[i])