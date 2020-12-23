from DB import SQLite as sql
from core import roles, stats as stat

idBaBot = 790899501845053461
idGetGems = 620558080551157770

idBASTION = 634317171496976395# 417445502641111051


async def memberjoin(member, channel):
    print(channel)
    if member.guild.id == idBASTION:
        channel_regle = member.guild.get_channel(417454223224209408)
        ID = member.id
        if sql.newPlayer(ID, "bastion") == "Le joueur a été ajouté !":
            msg = ":blue_square: Bienvenue {0} sur Bastion! :blue_square: \nNous sommes ravis que tu aies rejoint notre communauté !".format(member.mention)
            msg += "\n\nMerci de lire les règles et le fonctionnement du serveur dans le salon {0}".format(channel_regle.mention)
            msg += "\nAjoute aussi ton parrain avec `!parrain <Nom>`\n▬▬▬▬▬▬▬▬▬▬▬▬"
            await roles.addrole(member, "Nouveau")
        else:
            msg = "▬▬▬▬▬▬ Bon retour parmis nous ! {0} ▬▬▬▬▬▬".format(member.mention)
            await roles.addrole(member, "Nouveau")
        stat.countCo()
        print("Welcome >> {0} a rejoint le serveur {1}".format(member.name, member.guild.name))
        await channel.send(msg)


def memberremove(member):
    ID = member.id
    if member.guild.id == idBASTION:
        stat.countDeco()
        sql.updateField(ID, "lvl", 0, "bastion")
        sql.updateField(ID, "xp", 0, "bastion")
    print("Welcome >> {0} a quitté le serveur {1}".format(member.name, member.guild.name))
    msg = "**{0}** nous a quitté, pourtant si jeune...".format(member.name)
    return msg
