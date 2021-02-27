from data.info import *
import os


def run():
	if(not os.path.exists(DIRS['user-data'])):
		pass

	BASS_DECODER.reader.decode_file(DIRS['CCF']['BASE'])

if __name__ == "__main__":
	run()