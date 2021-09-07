import requests
from core import gestion as ge

SECRET_KEY = open("api/key.txt", "r").read().replace("\n", "")
headers = {'access_token': SECRET_KEY}


async def memberjoin(member, channel):
    if member.guild.id == ge.guildID[0]:
        channel_regle = member.guild.get_channel(417454223224209408)
        ID = member.id
        req = requests.get('http://{ip}/users/playerid/{discord_id}'.format(ip=ge.API_IP, discord_id=ID)).json()
        if req['error'] == 404:
            requests.post('http://{ip}/users/create/?discord_id={discord_id}'.format(ip=ge.API_IP, discord_id=ID), headers=headers)
            msg = ":blue_square: Bienvenue {0} sur Bastion! :blue_square: \nNous sommes ravis que tu aies rejoint notre communauté !".format(member.mention)
            msg += "\n\nMerci de lire les règles et le fonctionnement du serveur dans le salon {0}".format(channel_regle.mention)
            msg += "\nAjoute aussi ton parrain avec `!parrain @pseudo`\n▬▬▬▬▬▬▬▬▬▬▬▬"
            await ge.addrole(member, "Nouveau")
        else:
            msg = "▬▬▬▬▬▬ Bon retour parmis nous ! {0} ▬▬▬▬▬▬".format(member.mention)
            await ge.addrole(member, "Nouveau")
        await channel.send(msg)
    else:
        msg = ":blue_square: Bienvenue {0} sur {1}! :blue_square:".format(member.mention, member.guild.name)
        msg += "\nAjoute aussi ton parrain avec `!parrain @pseudo`\n▬▬▬▬▬▬▬▬▬▬▬▬"
        await channel.send(msg)


async def memberremove(member, channel):
    ID = member.id
    if member.guild.id == ge.guildID[0]:
        PlayerID = requests.get('http://{ip}/users/playerid/{discord_id}'.format(ip=ge.API_IP, discord_id=ID)).json()['ID']
        balXP = int(requests.get('http://{ip}/users/xp/{player_id}'.format(ip=ge.API_IP, player_id=PlayerID)).text)
        balLvl = int(requests.get('http://{ip}/users/level/{player_id}'.format(ip=ge.API_IP, player_id=PlayerID)).text)

        requests.put('http://{ip}/users/xp/{player_id}/{nb}'.format(ip=ge.API_IP, player_id=PlayerID, nb=-balXP), headers=headers)
        requests.put('http://{ip}/users/level/{player_id}/{nb}'.format(ip=ge.API_IP, player_id=PlayerID, nb=-balLvl), headers=headers)
    msg = "**{0}** nous a quitté, pourtant si jeune...".format(member.name)
    await channel.send(msg)
