# Module SQLite
# Version 1.0
import discord
import sqlite3 as sql
import datetime as dt
import time as t
import json


DB_NOM = 'bastionDB'


def nom_ID(nom):
    """Convertis un nom en ID discord """
    if len(nom) == 21 :
        ID = int(nom[2:20])
    elif len(nom) == 22 :
        ID = int(nom[3:21])
    elif len(nom) == 18:
        ID = int(nom)
    else :
        print("DB >> mauvais nom")
        ID = -1
    return(ID)


# ===============================================================================
# Ouverture du fichier DB
# ===============================================================================
conn = sql.connect('DB/{}.db'.format(DB_NOM))


# ===============================================================================
# Initialisation et vérification de la DB
# ===============================================================================
def init():
    # Liste des tables
    with open("DB/DBlist.json", "r") as f:
        list = json.load(f)
    for one in list:
        # Ouverture du template de la table en cours
        with open("DB/Templates/{}Template.json".format(one), "r") as f:
            t = json.load(f)
        cursor = conn.cursor()
        # Création du script
        script = "CREATE TABLE IF NOT EXISTS {}(".format(one)
        i = 0
        PRIMARYKEY = ""
        PRIMARYKEYlink = ""
        link = ""
        for x in t:
            if i != 0:
                script += ", "
            y = t[x].split("_")
            if len(y) > 1:
                if y[0] == "ID":
                    script += "{0} {1} NOT NULL".format(x, y[1])
                    link = "FOREIGN KEY(ID) REFERENCES IDs(ID)"
                elif y[0] == "PRIMARYKEY":
                    script += "{0} {1} NOT NULL".format(x, y[1])
                    PRIMARYKEY = "{}".format(x)
                elif y[0] == "link":
                    script += "{0} INTEGER NOT NULL".format(x)
                    PRIMARYKEYlink = "{}".format(x)
                    link = "FOREIGN KEY({1}) REFERENCES {0}({1})".format(y[1], x)
            else:
                script += "{0} {1}".format(x, t[x])
            i += 1
        # Configuration des clés primaires
        if PRIMARYKEY != "" and PRIMARYKEYlink != "":
            script += ", PRIMARY KEY ({}, {})".format(PRIMARYKEY, PRIMARYKEYlink)
        elif PRIMARYKEY != "" and PRIMARYKEYlink == "":
            script += ", PRIMARY KEY ({})".format(PRIMARYKEY)
        elif PRIMARYKEY == "" and PRIMARYKEYlink != "":
            script += ", PRIMARY KEY ({})".format(PRIMARYKEYlink)
        if link != "":
            script += ", {}".format(link)
        script += ")"
        # éxécution du script pour la table en cours
        cursor.execute(script)
        conn.commit()
    # Quand toute les tables ont été créée (si elles n'existait pas), envoie un message de fin
    return "SQL >> DB initialisée"


# -------------------------------------------------------------------------------
def checkField():
    # Init de la variable flag
    flag = 0
    FctCheck = False
    while not FctCheck:
        try:
            FctCheck = True
            # Liste des tables
            with open("DB/DBlist.json", "r") as f:
                list = json.load(f)
            for one in list:
                # Ouverture du template de la table en cours
                with open("DB/Templates/{}Template.json".format(one), "r") as f:
                    t = json.load(f)
                cursor = conn.cursor()
                # Récupération du nom des colonnes de la table en cours
                cursor.execute("PRAGMA table_info({0});".format(one))
                rows = cursor.fetchall()

                # Suppression
                for x in rows:
                    if x[1] not in t:
                        script = "ALTER TABLE {0} RENAME TO {0}_old".format(one)
                        cursor.execute(script)
                        init()
                        cursor.execute("PRAGMA table_info({0}_old);".format(one))
                        temp = ""
                        for z in cursor.fetchall():
                            if temp == "":
                                temp += "{}".format(z[1])
                            else:
                                temp += ", {}".format(z[1])
                        script = "INSERT INTO {0} ({1})\n    SELECT {1}\n    FROM {0}_old".format(one, temp)
                        cursor.execute(script)
                        cursor.execute("DROP TABLE {}_old".format(one))
                        conn.commit()
                        flag = "sup"+str(flag)

                # Type & add
                for x in t:
                    check = False
                    NotCheck = False
                    y = t[x].split("_")
                    for row in rows:
                        if row[1] == x:
                            if len(y) > 1:
                                if row[2] == y[1]:
                                    check = True
                                elif y[0] == "link":
                                    if row[2] == "INTEGER":
                                        check = True
                                    else:
                                        NotCheck = True
                                else:
                                    NotCheck = True
                            else:
                                if row[2] == t[x]:
                                    check = True
                                else:
                                    NotCheck = True
                    if NotCheck:
                        script = "ALTER TABLE {0} RENAME TO {0}_old".format(one)
                        cursor.execute(script)
                        init()
                        cursor.execute("PRAGMA table_info({0}_old);".format(one))
                        temp = ""
                        for z in cursor.fetchall():
                            if temp == "":
                                temp += "{}".format(z[1])
                            else:
                                temp += ", {}".format(z[1])
                        script = "INSERT INTO {0} ({1})\n    SELECT {1}\n    FROM {0}_old".format(one, temp)
                        cursor.execute(script)
                        cursor.execute("DROP TABLE {}_old".format(one))
                        conn.commit()
                        flag = "type"+str(flag)
                    elif not check:
                        if len(y) > 1:
                            temp = y[1]
                        else:
                            temp = y[0]
                        script = "ALTER TABLE {0} ADD COLUMN {1} {2}".format(one, x, temp)
                        cursor.execute(script)
                        flag = "add"+str(flag)
        except:
            FctCheck = False
    return flag


# ===============================================================================
# Gestion des utilisateurs
# ===============================================================================
def get_PlayerID(ID, nameDB = None):
    """
    Permet de convertir un ID discord en PlayerID interne à la base de données
    """
    if nameDB == None:
        script = "SELECT * FROM IDs WHERE ID_discord = {}".format(ID)
    else:
        script = "SELECT ID, id{0} FROM {0} JOIN IDs USING(ID) WHERE ID_discord = {1}".format(nameDB, ID)
    cursor = conn.cursor()
    cursor.execute(script)
    rows = cursor.fetchall()
    if rows == []:
        # Le PlayerID n'as pas été trouvé. Envoie un code Erreur
        return "Error 404"
    else:
        for x in rows:
            return "{}".format(x[0])


# -------------------------------------------------------------------------------
def userID(i, nameDB = None):
    if nameDB == None:
        nameDB = "bastion"
    script = "SELECT ID_discord FROM {1} JOIN IDs USING(ID) WHERE id{1} = '{0}'".format(i, nameDB)
    cursor = conn.cursor()
    cursor.execute(script)
    ID = cursor.fetchall()
    return ID[0][0]


# -------------------------------------------------------------------------------
def newPlayer(ID, nameDB = None):
    """
    Permet d'ajouter un nouveau joueur à la base de donnée en fonction de son ID.

    ID: int de l'ID du joueur
    """
    if nameDB == None:
        nameDB = "bastion"

    with open("DB/Templates/{}Template.json".format(nameDB), "r") as f:
        t = json.load(f)

    PlayerID = get_PlayerID(ID)
    cursor = conn.cursor()
    if PlayerID == "Error 404":
        # Init du joueur avec les champs de base
        script = "INSERT INTO IDs (ID_discord) VALUES ({})".format(ID)
        cursor.execute(script)
        conn.commit()
        PlayerID = get_PlayerID(ID)
        data = "ID"
        values = PlayerID
        for x in t:
            if x == "arrival":
                data += ", {}".format(x)
                values += ", '{}'".format(str(dt.date.today()))
            elif x != "id{}".format(nameDB) and x != "ID":
                data += ", {}".format(x)
                if "INTEGER" in t[x]:
                    values += ", 0"
                else:
                    values += ", NULL"
        script = "INSERT INTO {0} ({1}) VALUES ({2})".format(nameDB, data, values)
        cursor.execute(script)
        conn.commit()
        return ("Le joueur a été ajouté !")
    else:
        # Init du joueur dans Bastion avec les champs de base
        script = "SELECT * FROM {0} WHERE ID = {1}".format(nameDB, PlayerID)
        cursor.execute(script)
        z = cursor.fetchall()
        if z == []:
            data = "ID"
            values = PlayerID
            for x in t:
                if x == "arrival":
                    data += ", {}".format(x)
                    values += ", '{}'".format(str(dt.date.today()))
                elif x != "id{}".format(nameDB) and x != "ID":
                    data += ", {}".format(x)
                    if "INTEGER" in t[x]:
                        values += ", 0"
                    else:
                        values += ", NULL"
            script = "INSERT INTO {0} ({1}) VALUES ({2})".format(nameDB, data, values)
            cursor.execute(script)
            conn.commit()
            return ("Le joueur a été ajouté !")
        else:
            return ("Le joueur existe déjà")


# ===============================================================================
# Compteur
# ===============================================================================
def countTotalMsg():
    # Donne le nombre total de messages écrit sur le discord de Bastion
    script = "SELECT SUM(nbmsg) FROM bastion"
    cursor = conn.cursor()
    cursor.execute(script)
    for a in cursor.fetchall():
        return a[0]


# -------------------------------------------------------------------------------
def countTotalXP():
    # Donne le nombre total de messages écrit sur le discord de Bastion
    script = "SELECT SUM(xp) FROM bastion"
    cursor = conn.cursor()
    cursor.execute(script)
    for a in cursor.fetchall():
        return a[0]


# -------------------------------------------------------------------------------
def countFilleul(ID):
    # Donne le nombre total de messages écrit sur le discord de Bastion
    script = "SELECT count(idbastion) FROM bastion WHERE parrain = {0}".format(int(ID))
    cursor = conn.cursor()
    cursor.execute(script)
    for a in cursor.fetchall():
        return a[0]


# -------------------------------------------------------------------------------
def listFilleul(ID):
    # Donne le nombre total de messages écrit sur le discord de Bastion
    script = "SELECT ID_discord FROM bastion JOIN IDs USING(ID) WHERE parrain = {0}".format(int(ID))
    cursor = conn.cursor()
    cursor.execute(script)
    value = cursor.fetchall()

    if value == []:
        return 0
    else:
        for a in value:
            return a[0]


# -------------------------------------------------------------------------------
def taille(nameDB = None):
    """Retourne la taille de la table selectionner"""
    if nameDB == None:
        nameDB = "bastion"
    cursor = conn.cursor()
    cursor.execute("PRAGMA table_info({0});".format(nameDB))
    rows = cursor.fetchall()
    script = "SELECT count({1}) FROM {0}".format(nameDB, rows[0][1])
    cursor.execute(script)
    for taille in cursor.fetchall():
        return taille[0]


# ===============================================================================
# Fonctions
# ===============================================================================
# Liste des tables dont l'enregistrement des données est spécifique
nameDBexcept = ["filleuls", "bastion_com_time"]


# -------------------------------------------------------------------------------
def updateField(ID, fieldName, fieldValue, nameDB = None):
    """
    Permet de mettre à jour la valeur fieldName par la fieldValue.

    ID: int de l'ID du joueur.
    fieldName: string du nom du champ à changer
    fieldValue: string qui va remplacer l'ancienne valeur
    """
    PlayerID = get_PlayerID(ID, "bastion")
    if PlayerID != "Error 404":
        if nameDB == None:
            nameDB = "bastion"
        cursor = conn.cursor()

        # Vérification que la donnée fieldName existe dans la table nameDB
        one = valueAt(ID, fieldName, nameDB)
        if one == 0:
            # print("DB >> Le champ n'existe pas")
            return "201"
        else:
            if nameDB == "bastion":
                IDname = "id{}".format(nameDB)
                script = "UPDATE {0} SET {1} = '{2}' WHERE {4} = '{3}'".format(nameDB, fieldName, fieldValue, PlayerID, IDname)
            else:
                cursor.execute("PRAGMA table_info({0});".format(nameDB))
                rows = cursor.fetchall()
                for x in rows:
                    if x[1] == "idbastion":
                        IDname = "bastion"
                script = "SELECT id{2} FROM {0} WHERE id{2} = '{1}'".format(nameDB, PlayerID, IDname)
                cursor.execute(script)
                for z in cursor.fetchall():
                    PlayerID = z[0]
                script = "UPDATE {0} SET {1} = '{2}' WHERE id{4} = '{3}'".format(nameDB, fieldName, fieldValue, PlayerID, IDname)
            for x in nameDBexcept:
                if x == nameDB:
                    if x == "bastion_com_time":
                        script = "UPDATE {0} SET Com_time = '{2}' WHERE Commande = '{1}' and id{4} = '{3}'".format(nameDB, fieldName, fieldValue, PlayerID, IDname)
                    else:
                        return "202"
            # print("==== updateField ====")
            # print(script)
            cursor.execute(script)
            conn.commit()
            return "200"
    else:
        return "404"


# -------------------------------------------------------------------------------
def valueAt(ID, fieldName, nameDB = None):
    """
    Permet de récupérer la valeur contenue dans le champ fieldName de ID

    ID: int de l'ID du joueur
    fieldName: string du nom du champ à chercher
    """
    if nameDB == None:
        nameDB = "bastion"
    PlayerID = get_PlayerID(ID, "bastion")
    if PlayerID != "Error 404":
        cursor = conn.cursor()

        if nameDB not in nameDBexcept:
            try:
                # Récupération de la valeur de fieldName dans la table nameDB
                script = "SELECT {1} FROM {0} WHERE id{0} = '{2}'".format(nameDB, fieldName, PlayerID)
                cursor.execute(script)
                value = cursor.fetchall()
            except:
                # Aucune données n'a été trouvé
                value = []
        else:
            fieldName2 = ""
            for x in nameDBexcept:
                if x == nameDB:
                    if x == "bastion_com_time":
                        fieldName2 = "Commande"
                        fieldName3 = "Com_time, Commande"
                        link = "bastion"
                    elif x == "filleuls":
                        fieldName2 = "ID_filleul"
                        fieldName3 = "ID_filleul"
                        link = "bastion"
            try:
                # Paramètre spécial (à mettre a la place du fieldName) permettant de retourner toutes les valeurs liées à un PlayerID dans la table nameDB
                if fieldName == "all":
                    script = "SELECT {1} FROM {0} JOIN {2} USING(id{2}) WHERE id{2} = '{3}'".format(nameDB, fieldName3, link, PlayerID)
                    # print(script)
                else:
                    # Récupération de la valeur de fieldName dans la table nameDB
                    script = "SELECT {5} FROM {0} JOIN {3} USING(id{3}) WHERE id{3} = '{4}' and {2} = '{1}'".format(nameDB, fieldName, fieldName2, link, PlayerID, fieldName3)
                    # print(script)
                cursor.execute(script)
                value = cursor.fetchall()
            except:
                # Aucune données n'a été trouvé
                value = []

        if value == []:
            return 0
        else:
            if fieldName == "all":
                return value
            else:
                return value[0]


# -------------------------------------------------------------------------------
def valueAtNumber(ID, fieldName, nameDB = None):
    if fieldName != "all":
        VAN = valueAt(ID, fieldName, nameDB)
        if VAN != 0 and VAN != None:
            VAN = VAN[0]
        return VAN
    else:
        return 0


# -------------------------------------------------------------------------------
def spam(ID, couldown, nameElem, nameDB = None):
    """Antispam """
    if nameDB == None:
        nameDB = "bastion_com_time"
    elif nameDB == "bastion":
        nameDB = "{}_com_time".format(nameDB)

    ComTime = valueAt(ID, nameElem, nameDB)
    if ComTime == 0 or ComTime == None:
        return True
    elif ComTime[0] != 0:
        time = ComTime[0]
    else:
        return True

    # on récupère la date de la dernière commande
    return(float(time) < t.time()-couldown)


# -------------------------------------------------------------------------------
def updateComTime(ID, nameElem, nameDB = None):
    """
    Met à jour la date du dernier appel à une fonction
    """
    if nameDB == None:
        nameDB = "bastion_com_time"
    elif nameDB == "bastion":
        nameDB = "{}_com_time".format(nameDB)
    else:
        return "Error 404"

    old_value = valueAtNumber(ID, nameElem, nameDB)
    try:
        if old_value != 0:
            new_value = t.time()
            updateField(ID, nameElem, new_value, nameDB)
            return 100
        else:
            print(add(ID, nameElem, t.time(), nameDB))
            return 101
    except:
        return 404


# -------------------------------------------------------------------------------
def add(ID, nameElem, nbElem, nameDB = None):
    """
    Permet de modifier le nombre de nameElem pour ID dans la table nameDB
    Pour en retirer mettez nbElemn en négatif
    """
    if nameDB == None:
        nameDB = "bastion"

    PlayerID = get_PlayerID(ID, "bastion")

    old_value = valueAt(ID, nameElem, nameDB)
    if old_value != 0:
        new_value = int(old_value[0]) + int(nbElem)
        if new_value < 0:
            new_value = 0
        updateField(ID, nameElem, new_value, nameDB)
        return 100
    else:
        cursor = conn.cursor()
        data = []
        with open("DB/Templates/{}Template.json".format(nameDB), "r") as f:
            t = json.load(f)
        for x in t:
            if x == "idbastion":
                data = "{}".format(x)
            else:
                data += ",{}".format(x)

        if nameDB not in nameDBexcept:
            values = "{}".format(PlayerID)
            for x in t:
                y = t[x].split("_")
                if len(y) > 1:
                    y2 = y[1]
                else:
                    y2 = y[0]
                if x == nameElem:
                    values += ",'{}'".format(nbElem)
                elif y2 == "INTEGER":
                    values = ",'0'"
                elif y2 == "TEXT":
                    values = ",''"
        else:
            if nameDB == "bastion_com_time":
                data = "idbastion, Commande, Com_time"
                values = "'{2}', '{0}', '{1}'".format(nameElem, nbElem, PlayerID)
            elif nameDB == "filleuls":
                data = "idbastion, ID_filleul"
                values = "{1}, {0}".format(nbElem, PlayerID)
        try:
            script = "INSERT INTO {0} ({1}) VALUES ({2})".format(nameDB, data, values)
            # print("==== add ====")
            # print(script)
            cursor.execute(script)
            conn.commit()
            return 101
        except:
            return 404
