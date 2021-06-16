from os import listdir
import json

general_dict_lang = dict()
for file in listdir("languages"):
    if ".json" in file:
        langname = file.replace(".json", "")
        path = "languages/"+file
        with open(path, encoding='utf-8') as json_file:
            data = json.load(json_file)
            general_dict_lang[langname] = data
