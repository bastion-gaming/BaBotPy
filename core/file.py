# Version 1.0
import os
import json

# •••••••••••••••••••••••••••••••••••••••
def exist(path):
	if os.path.exists(path):
		return True
	else:
		return False


# •••••••••••••••••••••••••••••••••••••••
def read(path):
	if exist(path):
		file = open(path, 'r', encoding='utf-8')
		return file
	else:
		print("Le fichier n'existe pas")
		return False


# •••••••••••••••••••••••••••••••••••••••
def write(path, data):
	if exist(path):
		file = open(path, 'w', encoding='utf-8')
		file.write(data)
		file.close()
		return True
	else:
		print("Le fichier n'existe pas")
		return False


# •••••••••••••••••••••••••••••••••••••••
def add(path, data):
	if exist(path):
		file = open(path, 'a', encoding='utf-8')
		file.write(data)
		file.close()
		return True
	else:
		print("Le fichier n'existe pas")
		return False


# •••••••••••••••••••••••••••••••••••••••
def delete(path):
	if exist(path):
		os.remove(path)
		return True
	else:
		print("Impossible de supprimer le fichier car il n'existe pas")
		return False


# •••••••••••••••••••••••••••••••••••••••
# ••••••••••••••• JSON ••••••••••••••••••
# •••••••••••••••••••••••••••••••••••••••

def json_read(path):
	if exist(path):
		file = read(path)
		data = json.load(file)
		file.close()
		return data
	else:
		print("Le fichier n'existe pas")
		return False
	
# •••••••••••••••••••••••••••••••••••••••
def json_write(path, data):
	if exist(path):
		file = open(path, 'w', encoding='utf-8')
		json.dump(data, file)
		file.close()
		return True
	else:
		print("Le fichier n'existe pas")
		return False