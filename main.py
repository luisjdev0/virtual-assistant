from data.info import *
import os


def run():
	global globaldata
	if(not os.path.exists(DIRS['user-data'])):
		BASS_DECODER.reader.decode_file(DIRS['CCF']['BASE'])

	BASS_DECODER.reader.decode_file(DIRS['CCF']['MAIN'])

	speak(f"Hasta pronto {globaldata['assistant-data']['user-alias']}")

if __name__ == "__main__":
	run()