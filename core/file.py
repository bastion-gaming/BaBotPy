# Version 1.1
import os
import json

# •••••••••••••••••••••••••••••••••••••••
def exist(path):
	if os.path.exists(path):
		return True
	else:
		return False


# •••••••••••••••••••••••••••••••••••••••
def open_read(path):
	if exist(path):
		file = open(path, 'r', errors="ignore")
		return file
	else:
		print(f"Le fichier {path} n'existe pas")
		return False


# •••••••••••••••••••••••••••••••••••••••
def read(path):
	if exist(path):
		file = open_read(path)
		return file.read()
	else:
		print(f"Le fichier {path} n'existe pas")
		return False


# •••••••••••••••••••••••••••••••••••••••
def write(path, data):
	if exist(path):
		file = open(path, 'w')
		file.write(data)
		file.close()
		return True
	else:
		print(f"Le fichier {path} n'existe pas")
		return False


# •••••••••••••••••••••••••••••••••••••••
def add(path, data):
	if exist(path):
		file = open(path, 'a')
		file.write(data)
		file.close()
		return True
	else:
		print(f"Le fichier {path} n'existe pas")
		return False


# •••••••••••••••••••••••••••••••••••••••
def create(path):
	file = open(path, 'w')
	file.close()
	return True


# •••••••••••••••••••••••••••••••••••••••
def createdir(path):
	if not os.path.exists(path):
		os.makedirs(path)
		return True
	return False


# •••••••••••••••••••••••••••••••••••••••
def delete(path):
	if exist(path):
		os.remove(path)
		return True
	else:
		print(f"Impossible de supprimer le fichier {path} car il n'existe pas")
		return False


# •••••••••••••••••••••••••••••••••••••••
# ••••••••••••••• JSON ••••••••••••••••••
# •••••••••••••••••••••••••••••••••••••••

def json_read(path):
	if exist(path):
		file = open_read(path)
		data = json.load(file)
		file.close()
		return data
	else:
		print(f"Le fichier {path} n'existe pas")
		return False
	
# •••••••••••••••••••••••••••••••••••••••
def json_write(path, data):
	if exist(path):
		file = open(path, 'w')
		json.dump(data, file)
		file.close()
		return True
	else:
		print(f"Le fichier {path} n'existe pas")
		return False

# •••••••••••••••••••••••••••••••••••••••
def json_loads(data):
	return json.loads(data)