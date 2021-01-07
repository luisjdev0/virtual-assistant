import os
from MODULES.first_init import initial_dates
from MODULES.command_manager import command_prompt, prompt

DIRS = {
	"SERIAL" : "res/serialization/",
	"DATA"   : "res/user_data/",
	"CMDS"   : "res/cmds/",
}


def run():

	if not os.path.isdir("res/"):
		os.mkdir("res/")

	#First Run
	for i in DIRS:
		if not os.path.isdir(DIRS[i]):
			os.mkdir(DIRS[i])
			print(f"Dir {i} created")

	initial_dates(DIRS["DATA"])
	print("\n")
	command_prompt()



if __name__ == "__main__":
	run()