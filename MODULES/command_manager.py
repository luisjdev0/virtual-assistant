from MODULES.SD import jl_reader
import os

def prompt(x = ""):
	return input(f"{x}-> ")

def command_prompt():
	command = ""
	while True:
		command = prompt().lower()

		if command == "exit":
			break

class cmd_manager:
	def __init__(self):
		