from sys import exc_info

class jl_reader:
	def __init__ (self, fkeys : dict, lkeys : dict, skeys : dict, fsep = '$', lsep = ':', thr_exc = False):

		self.fkeys = fkeys
		self.lkeys = lkeys
		self.skeys = skeys
		self.fsep = fsep
		self.lsep = lsep
		self.thr_exc = thr_exc

	def __decode_lkeys(self, line):
		if line.find(self.lsep) == -1:
			return (None, None)
		else:
			word = line[line.find(self.lsep) + 1: line.find(self.lsep, line.find(self.lsep) + 1)]
			line_words = word.split(' ')

			if line_words[0] in self.lkeys:
				return (str(word), str(self.lkeys[line_words[0]](line_words[1:len(line_words)])))
			else:
				print(f"No existe una función lista llamada '{line_words[0]}'")
				return (None, None)

	def __sentence_to_list(self, sentence):
		return sentence.split(' ')

	def __list_to_sentence(self, list_sentence):
		word = ""
		for i in list_sentence:
			word += f"{str(i)} "

		return word


	def decode_line(self, line):
		if line.split(' ')[0] == ' ' or line.split(' ')[0] == '':
			return None
		try:
			line_words = line.split(' ')
			sentence = []

			#Decode SKEYS
			for i in range(1, len(line_words)):
				if line_words[i].find(self.fsep) != -1:
					if line_words[i].replace(self.fsep, '') in self.skeys:
						sentence.append(self.skeys[line_words[i].replace(self.fsep, '')])
					else:
						sentence.append(line_words[i])
				else:
					sentence.append(line_words[i])

			#DECODE LKEYS
			word = self.__list_to_sentence(sentence)
			lkey = self.__decode_lkeys(word)

			if lkey != (None, None):
				word = word.replace(lkey[0], lkey[1]).replace(':', '')

			sentence = self.__sentence_to_list(word)
			#Decode FKEYS
			if line_words[0].find(self.lsep) == -1:
				if line_words[0] in self.fkeys:
					return self.fkeys[line_words[0]](self.__list_to_sentence(sentence))
				else:
					print(f"No existe una función llamada '{line_words[0]}'")
		except: 
			if not self.thr_exc:
				print(f"Hubo un error: {exc_info()[1]}")
			else:
				raise exc_info()[0](exc_info([1]))

	def decode_file(self, file_path):
		outputs = []
		file = open(file_path, "r", encoding='UTF-8')
		lines = list(file.readlines())

		for i in range(len(lines)):
			lines[i] = lines[i].replace("\n", '')
			outputs.append(self.decode_line(lines[i]))

		return outputs