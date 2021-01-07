import os
from sys import exc_info
import json
from MODULES.load_jls import load_jls_info

def initial_dates(data_path):

	jfpath = data_path + "assistant_info.json"
	data = {}

	if not os.path.isfile(jfpath):

		info = load_jls_info()

		while True:

			try:
				info.reader.decode_file("res/cmds/init_information.jls")
				break

			except Exception:
				os.system("clear")

				print("Perdón, ocurrió un error.")
				print("Para asegurarme de que tendré la información correcta, te la volveré a solicitar")
				print("\n")
				print("Aquí información de lo que ocurrió")
				print(exc_info()[1])
				print("\n")

		print("\n")

		try:
			print("Guardando la información...")
			json.dump(info.data, open(jfpath, "w"))

			print(f"Información guardada {info.data['alias']}.")

		except Exception:
			print(f"No pude guardar la información {info.data['alias']}")
			print(exc_info()[1])

	

	os.system("clear")
	try:

		print("Bienvenido, Cargando la información")
		data = json.load(open(jfpath, "r"))

		print(f"Información cargada {data['alias']}")

	except:

		print("No pude cargar la información.")
		print(exc_info()[1])
