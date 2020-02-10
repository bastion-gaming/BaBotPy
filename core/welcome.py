from DB import SQLite as sql
from core import roles, stats as stat

idBaBot = 604776153458278415
idGetGems = 620558080551157770

idBASTION = 417445502641111051
idchannel_botplay = 533048015758426112
idchannel_nsfw = 425391362737700894
idcategory_admin = 417453424402235407


async def memberjoin(member, channel):
    if member.guild.id == idBASTION:
        channel_regle = member.guild.get_channel(417454223224209408)
        ID = member.id
        if sql.newPlayer(ID, "bastion") == "Le joueur a été ajouté !":
            msg = ":black_small_square:Bienvenue {0} sur Bastion!:black_small_square: \n\n\nNous sommes ravis que tu aies rejoint notre communauté !".format(member.mention)
            msg += "\nTu es attendu : \n\n:arrow_right: Sur {0}\nAjoute aussi ton parrain avec `!parrain <Nom>`\n\n=====================".format(channel_regle.mention)
            await roles.addrole(member, "Nouveau")
        else:
            msg = "===================== Bon retour parmis nous ! {0} =====================".format(member.mention)
            await roles.addrole(member, "Nouveau")
        stat.countCo()
    else:
        msg = "Bienvenue {} sur {}".format(member.mention, member.guild.name)
    print("Welcome >> {} a rejoint le serveur {}".format(member.name, member.guild.name))
    await channel.send(msg)


def memberremove(member):
    ID = member.id
    gems = sql.valueAtNumber(ID, "gems", "gems")
    idBot = idBaBot
    pourcentage = 0.3
    if member.guild.id == idBASTION:
        stat.countDeco()
        sql.updateField(ID, "lvl", 0, "bastion")
        sql.updateField(ID, "xp", 0, "bastion")
    print("Welcome >> {} a quitté le serveur {}".format(member.name, member.guild.name))
    try:
        transfert = gems * pourcentage
        sql.addGems(idBot, int(transfert))
        sql.addGems(ID, int(-transfert))
    except:
        print("Welcome >> Echec du transfert de gems")
    msg = "**{0}** nous a quitté, pourtant si jeune...".format(member.name)
    return msg
