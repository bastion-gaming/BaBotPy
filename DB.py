import discord
from tinydb import TinyDB, Query
import datetime as dt

DB_NOM = 'bastionDB.json'
db = TinyDB(DB_NOM)
inv = dict()

def dbExist():
    """
    Retourne True ou False en fonction de si la db existe.
    """
    try:
        with open(DB_NOM): pass
    except IOError:
        return False
    return True

def newPlayer(ID):
    """
    Permet d'ajouter un nouveau joueur à la base de donnée en fonction de son ID.

    ID: int de l'ID du joueur
    """

    if db.search(Query().ID == ID) == []:
        #Init du joueur avec les champs de base
        #########################MODIFIER ICI SI NVX CHAMPS#####################
        db.insert({'ID': ID, 'arrival': str(dt.datetime.now()),'com_time': 0,'gems':0, 'inventory':inv})
        ########################################################################
        print("Le joueur a été ajouté !")
        return 100
    else:
        print("Le joueur existe déjà")
        return 101


def updateField(ID, fieldName, fieldValue):
    """
    Permet de mettre à jour la valeur fieldName par la fieldValue.

    ID: int de l'ID du joueur.
    fieldName: string du nom du champ à changer
    fieldValue: string qui va remplacer l'ancienne valeur
    """
    if db.search(getattr(Query(),fieldName)) == []:
        print("Le champ n'existe pas")
        return "201"
    else:
        db.update({fieldName: fieldValue}, Query().ID == ID)
        print("Le champ a été mis à jour")
        return "200"


def valueAt(ID, fieldName):
    """
    Permet de récupérer la valeur contenue dans le champ fieldName de ID

    ID: int de l'ID du joueur
    fieldName: string du nom du champ à chercher
    """
    return db.search(Query().ID == ID)[0][fieldName]

async def count(message):
    l=len(db)
    if l == 0:
        await message.channel.send('Aucun utilisaeur enregistrer dans la BDD')
    else:
        await message.channel.send(f'{l} utilisateur inscrit')
