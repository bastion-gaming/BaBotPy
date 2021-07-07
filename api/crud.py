from sqlalchemy.orm import Session
from sqlalchemy.sql import func
from sqlalchemy import text
import time as t, datetime as dt
from operator import itemgetter
from . import models, schemas


# -------------------------------------------------------------------------------
def get_user_discord_id(db: Session, discord_id: str):
    return db.query(models.TableCore).filter(models.TableCore.discord_id == discord_id).first()


# -------------------------------------------------------------------------------
def get_user_by_name(db: Session, name: str):
    return db.query(models.TableCore).filter(models.TableCore.pseudo == name).first()


# -------------------------------------------------------------------------------
def get_user(db: Session, PlayerID: int):
    return db.query(models.TableCore).filter(models.TableCore.playerid == PlayerID).first()


# -------------------------------------------------------------------------------
def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.TableCore).offset(skip).limit(limit).all()


# -------------------------------------------------------------------------------
def get_user_old(db: Session, PlayerID: int):
    return db.query(models.TableCoreOld).filter(models.TableCoreOld.playerid == PlayerID).first()


# -------------------------------------------------------------------------------
def get_users_old(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.TableCoreOld).offset(skip).limit(limit).all()


# -------------------------------------------------------------------------------
def get_godchilds(db: Session, PlayerID: int):
    return db.query(models.TableCore).filter(models.TableCore.godparent == PlayerID).all()


# -------------------------------------------------------------------------------
def get_PlayerID(db: Session, discord_id: str, platform: str):
    return get_user_discord_id(db=db, discord_id=discord_id)


# ===============================================================================
# Createur
# ===============================================================================
def create_user(db: Session, discord_id):
    id = 1
    boucleID = True
    while boucleID:
        if not get_user(db, id):
            boucleID = False
        else:
            id += 1
    db_user = models.TableCore(
        playerid = id,
        discord_id = discord_id,
        arrival = str(dt.date.today()),
        level = 0,
        xp = 0,
        devise = 500,
        super_devise = 1,
        godparent = 0,
        nbreaction = 0,
        nbmsg = 0,
        core_old = [],
        com_time = []
    )
    db_user_old = models.TableCoreOld(
        playerid = id,
        discord_id = discord_id,
        level = 0,
        xp = 0
    )
    db.add(db_user)
    db.commit()
    db.add(db_user_old)
    db.commit()
    db.refresh(db_user)
    return db_user


# -------------------------------------------------------------------------------
def create_com_time(db: Session, user: schemas.TableComTime):
    db_user = models.GemsComTime(
        playerid = user.playerid,
        command = user.command,
        time = user.time
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


# ===============================================================================
# Compteur
# ===============================================================================
def countTotalDevise(db: Session):
    return db.query(func.sum(models.TableCore.devise).label("total_devise")).first()


# -------------------------------------------------------------------------------
def countTotalSuperDevise(db: Session):
    return db.query(func.sum(models.TableCore.super_devise).label("total_super_devise")).first()


# -------------------------------------------------------------------------------
def countTotalMsg(db: Session):
    return db.query(func.sum(models.TableCore.nbmsg).label("total_message")).first()


# -------------------------------------------------------------------------------
def countTotalXP(db: Session):
    return db.query(func.sum(models.TableCore.xp).label("total_xp")).first()


# -------------------------------------------------------------------------------
def taille(db: Session):
    """Retourne la taille de la table selectionnée"""
    return db.query(func.count(models.TableCore.playerid).label("taille")).first()


# -------------------------------------------------------------------------------
def countFilleul(db: Session, PlayerID: int):
    """Retourne la taille de la table selectionnée"""
    list = get_godchilds(db, PlayerID)
    nbg = len(list)
    if nbg != None:
        return nbg
    else:
        return 0


# ===============================================================================
# Classement
# ===============================================================================
def topxp(db: Session, min = 0, max = 10):
    UserList = []
    res = []
    DBtaille = taille(db=db)
    if DBtaille == {}:
        DBtaille = 0
    else:
        DBtaille = int(DBtaille['taille'])
    users = get_users(db=db, skip=0, limit=DBtaille)
    for user in users:
        IDi = int(user.discord_id)
        nbMsg = user.nbmsg
        nbReac = user.nbreaction
        XP = user.xp
        mylvl = user.level
        Arrival = user.arrival
        UserList.append([IDi, XP, nbMsg, Arrival, mylvl, nbReac])
    UserList = sorted(UserList, key=itemgetter(1), reverse=True)
    i=1
    for one in UserList:
        res.append({"discord_id": one[0], "nbmsg": one[2], "nbreaction": one[5], "xp": one[1], "level": one[4], "arrival": one[3]})
        if i >= max:
            return res
        i+=1
    return res


# -------------------------------------------------------------------------------
def toplevel(db: Session, min = 0, max = 10):
    UserList = []
    res = []
    DBtaille = taille(db=db)
    if DBtaille == {}:
        DBtaille = 0
    else:
        DBtaille = int(DBtaille['taille'])
    users = get_users(db=db, skip=0, limit=DBtaille)
    for user in users:
        IDi = int(user.discord_id)
        nbMsg = user.nbmsg
        nbReac = user.nbreaction
        XP = user.xp
        mylvl = user.level
        Arrival = user.arrival
        UserList.append([IDi, XP, nbMsg, Arrival, mylvl, nbReac])
    UserList = sorted(UserList, key=itemgetter(4), reverse=True)
    i=1
    for one in UserList:
        res.append({"discord_id": one[0], "nbmsg": one[2], "nbreaction": one[5], "xp": one[1], "level": one[4], "arrival": one[3]})
        if i >= max:
            return res
        i+=1
    return res


# -------------------------------------------------------------------------------
def topmsg(db: Session, min = 0, max = 10):
    UserList = []
    res = []
    DBtaille = taille(db=db)
    if DBtaille == {}:
        DBtaille = 0
    else:
        DBtaille = int(DBtaille['taille'])
    users = get_users(db=db, skip=0, limit=DBtaille)
    for user in users:
        IDi = int(user.discord_id)
        nbMsg = user.nbmsg
        nbReac = user.nbreaction
        XP = user.xp
        mylvl = user.level
        Arrival = user.arrival
        UserList.append([IDi, XP, nbMsg, Arrival, mylvl, nbReac])
    UserList = sorted(UserList, key=itemgetter(2), reverse=True)
    i=1
    for one in UserList:
        res.append({"discord_id": one[0], "nbmsg": one[2], "nbreaction": one[5], "xp": one[1], "level": one[4], "arrival": one[3]})
        if i >= max:
            return res
        i+=1
    return res


# -------------------------------------------------------------------------------
def topreaction(db: Session, min = 0, max = 10):
    UserList = []
    res = []
    DBtaille = taille(db=db)
    if DBtaille == {}:
        DBtaille = 0
    else:
        DBtaille = int(DBtaille['taille'])
    users = get_users(db=db, skip=0, limit=DBtaille)
    for user in users:
        IDi = int(user.discord_id)
        nbMsg = user.nbmsg
        nbReac = user.nbreaction
        XP = user.xp
        mylvl = user.level
        Arrival = user.arrival
        UserList.append([IDi, XP, nbMsg, Arrival, mylvl, nbReac])
    UserList = sorted(UserList, key=itemgetter(5), reverse=True)
    i=1
    for one in UserList:
        res.append({"discord_id": one[0], "nbmsg": one[2], "nbreaction": one[5], "xp": one[1], "level": one[4], "arrival": one[3]})
        if i >= max:
            return res
        i+=1
    return res


# ===============================================================================
# Fonctions
# ===============================================================================
def in_table(db: Session, nameTable, fieldName, filtre = None, filtreValue = None):
    """
    string          nameTable
    string/tab      fieldname
    string/tab      filtre
    string/tab      filtreValue
    """
    script = ""

    if type(fieldName) is str:
        script = "SELECT {0} FROM {1}".format(fieldName, nameTable)
    elif type(fieldName) is list:
        script += "SELECT {0}".format(fieldName[0])
        for i in range(1, len(filtre)):
            script += ",{0}".format(fieldName[i])
        script += " FROM {0}".format(nameTable)

    if filtre is not None:
        if type(filtre) is list:
            script += " WHERE {0} = '{1}'".format(filtre[0], filtreValue[0])
            for i in range(1, len(filtre)):
                script += " AND {0} = '{1}'".format(filtre[i], filtreValue[i])
        elif type(filtre) is str:
            script += " WHERE {0} = '{1}'".format(filtre, filtreValue)
    # print(script)
    script = text(script)
    rows = db.execute(script).fetchall()
    # print(rows)
    if rows == []:
        return False
    for r in rows:
        rs = dict()
        for x in r.keys():
            rs[x] = r[x]
        return rs


# -------------------------------------------------------------------------------
def spam(db: Session, PlayerID, couldown, Command):
    """Antispam """
    nameTable = "com_time"
    ComTime = value(db, PlayerID, nameTable, "time", "command", Command)
    time = float(ComTime)
    if not ComTime or ComTime == None:
        return True
    elif time != 0:
        return(float(time) < t.time()-couldown)
    else:
        return True


# -------------------------------------------------------------------------------
def updateComTime(db: Session, PlayerID, Command):
    """
    Met à jour la date du dernier appel à une fonction
    """
    nameTable = "com_time"

    old_value = value(db, PlayerID, nameTable, "time", "command", Command)
    try:
        if old_value is not False:
            time = t.time()
            update(db, PlayerID, nameTable, "time", time, "command", Command)
            return {'error': 0, 'action': 'update success', 'time': time}
        else:
            comtime_model = models.TableComTime(
                playerid = PlayerID,
                command = Command,
                time = str(t.time())
            )
            create_com_time(db, comtime_model)
            return {'error': 0, 'action': 'update fail -> create success', 'time': comtime_model.time}
    except:
        return {'error': 404, 'action': 'echec'}


# -------------------------------------------------------------------------------
def value(db: Session, PlayerID, nameTable, fieldName, filtre = None, filtreValue = None, order = None):
    """
    int             PlayerID: id du joueur dans la base de données
    string          nameTable: Nom de la table
    string          fieldName: string du nom du champ à chercher
    string/tab      filtre: liste des filtres WHERE
    string/tab      filtreValue: liste des valeurs de chaque filtre
    tab             order: paramètre de tri
    """
    value = []
    mefn = ''

    try:
        # Récupération de la valeur de fieldName dans la table nameTable
        if type(fieldName) is str:
            mefn = fieldName
        elif type(fieldName) is list:
            for i in range(0, len(fieldName)):
                if i > 0:
                    mefn += ", "
                mefn += "{}".format(fieldName[i])
        else:
            return False
        script = "SELECT {1} FROM {0}".format(nameTable, mefn)
        script += " WHERE playerid = '{0}'".format(PlayerID)
        if filtre is not None:
            if type(filtre) is list:
                for i in range(0, len(filtre)):
                    script += " AND {0} = '{1}'".format(filtre[i], filtreValue[i])
            elif type(filtre) is str:
                script += " AND {0} = '{1}'".format(filtre, filtreValue)
        if order is not None:
            script += " ORDER BY {0}".format(order)
        # print(script)
        script = text(script)
        value = db.execute(script).fetchall()
    except:
        # Aucune données n'a été trouvé
        value = []

    # print("==== value ====")
    # print(value)
    if value == []:
        return False
    else:
        if len(value[0]) == 1:
            return value[0][0]
        else:
            return value[0]


# -------------------------------------------------------------------------------
def valueAll(db: Session, PlayerID, nameTable, fieldName, filtre = None, filtreValue = None, order = None):
    """
    int             PlayerID: id du joueur dans la base de données
    string          nameTable: Nom de la table
    string/tab      fieldName: string du nom du/des champ(s) à chercher
    string/tab      filtre: liste des filtres WHERE
    string/tab      filtreValue: liste des valeurs de chaque filtre
    tab             order: paramètre de tri
    """
    mefn = ""

    try:
        # Récupération de la valeur de fieldName dans la table nameTable
        if type(fieldName) is str:
            mefn = fieldName
        elif type(fieldName) is list:
            for i in range(0, len(fieldName)):
                if i > 0:
                    mefn += ", "
                mefn += "{}".format(fieldName[i])
        else:
            return False
        script = "SELECT {1} FROM {0}".format(nameTable, mefn)
        script += " WHERE playerid = '{0}'".format(PlayerID)
        if filtre is not None:
            if type(filtre) is list:
                for i in range(0, len(filtre)):
                    script += " AND {0} = '{1}'".format(filtre[i], filtreValue[i])
            elif type(filtre) is str:
                script += " AND {0} = '{1}'".format(filtre, filtreValue)
        if order is not None:
            script += " ORDER BY {0}".format(order)
        # print(script)
        script = text(script)
        value = db.execute(script).fetchall()
    except:
        # Aucune données n'a été trouvé
        value = []

    # print(value)
    if value == []:
        return False
    else:
        return value


# -------------------------------------------------------------------------------
def update(db: Session, PlayerID, nameTable, fieldName, fieldValue, filtre = None, filtreValue = None, order = None):
    """
    int             PlayerID: id du joueur dans la base de données
    string          nameTable: Nom de la table
    string/tab      fieldName: nom du/des champ(s) à chercher
    string/tab      fieldValue: valeur associé au fieldName
    string/tab      filtre: liste des filtres WHERE
    string/tab      filtreValue: liste des valeurs de chaque filtre
    tab             order: paramètre de tri
    """
    mefdv = ""
    script = ""
    val = value(db, PlayerID, nameTable, fieldName, filtre, filtreValue, order)
    # Vérification
    if val != [] or val is not False:
        # Mise en forme des data et values
        if type(fieldName) is list:
            for i in range(0, len(fieldName)):
                if i > 0:
                    mefdv += ", "
                mefdv += "{d} = '{v}'".format(d=fieldName[i], v=fieldValue[i])
        else:
            mefdv = "{d} = '{v}'".format(d=fieldName, v=fieldValue)
        # Mise en forme des filtres
        sF = "WHERE playerid = '{0}'".format(PlayerID)
        if filtre is not None:
            if type(filtre) is list:
                for i in range(0, len(filtre)):
                    sF += " AND {0} = '{1}'".format(filtre[i], filtreValue[i])
            elif type(filtre) is str:
                sF += " AND {0} = '{1}'".format(filtre, filtreValue)

        try:
            script = text("UPDATE {n} SET {u} {f}".format(n=nameTable, f=sF, u=mefdv))
            # print("==== updateField ====")
            # print(script)
            db.execute(script)
            db.commit()
            return True
        except:
            print('Error SQL update: {}'.format(script))
            return False
    else:
        return False
