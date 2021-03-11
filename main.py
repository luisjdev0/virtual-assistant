from data.info import *
import os


def run():
	global globaldata
	CCF_extra_functions.set_required_folders()
	if(not os.path.exists(DIRS['user-data'])):
		BASS_DECODER.reader.decode_file(DIRS['CCF']['BASE'])

	BASS_DECODER.reader.decode_file(DIRS['CCF']['MAIN'])

if __name__ == "__main__":
	run()
	
	#Limpiar audios
	try:
		for i in os.listdir(DIRS['folders']['audio']):
			os.remove(f"{DIRS['folders']['audio']}/{i}")
	except:
		print(f"No se pudo eliminar el contenido de {DIRS['folders']['audio']}")