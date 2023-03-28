import discord
import requests
from core import gestion as ge

SECRET_KEY = open("api/key.txt", "r").read().replace("\n", "")
headers = {'access_token': SECRET_KEY}

def addxp(ID, nb):
    PlayerID = requests.get('http://{ip}/users/playerid/{discord_id}'.format(ip=ge.API_IP, discord_id=ID)).json()['ID']
    requests.put('http://{ip}/users/xp/{player_id}/{nb}'.format(ip=ge.API_IP, player_id=PlayerID, nb=nb), headers=headers)


def addmsg(ID, nb):
    PlayerID = requests.get('http://{ip}/users/playerid/{discord_id}'.format(ip=ge.API_IP, discord_id=ID)).json()['ID']
    requests.put('http://{ip}/users/msg/{player_id}/{nb}'.format(ip=ge.API_IP, player_id=PlayerID, nb=nb), headers=headers)


def addreaction(ID, nb):
    PlayerID = requests.get('http://{ip}/users/playerid/{discord_id}'.format(ip=ge.API_IP, discord_id=ID)).json()['ID']
    requests.put('http://{ip}/users/reaction/{player_id}/{nb}'.format(ip=ge.API_IP, player_id=PlayerID, nb=nb), headers=headers)


def xpmsg(message):
    ID = message.author.id
    checkInfo(ID)
    if message.mention_everyone is False:
        lw = message.content.split()
        nb = (len(lw)//15)+1
        if nb <= 0:
            nb = 1
        elif nb > 6:
            nb = 6
        addxp(ID, nb)
    else:
        addxp(ID, 1)
    addmsg(ID, 1)
    return True


def addxp_voc(ID, time):
    PlayerID = requests.get('http://{ip}/users/playerid/{discord_id}'.format(ip=ge.API_IP, discord_id=ID)).json()['ID']
    time = int(time)
    if time <= 240:
        XP = time
    else:
        retime = int((time - 240)/2)
        if retime <= 30:
            XP = 240 + retime
        else:
            retime = int((retime - 30)/4)
            XP = 270 + retime
    requests.put('http://{ip}/users/xp/{player_id}/{nb}'.format(ip=ge.API_IP, player_id=PlayerID, nb=XP), headers=headers)


def lvlPalier(lvl):
    if lvl <= 0:
        return 10
    else:
        return int(30 * (lvl)**(2.5))


# BaBot | vérification du level
async def checklevel(message):
    ID = message.author.id
    Nom = message.author.name
    member = message.guild.get_member(ID)
    try:
        PlayerID = requests.get('http://{ip}/users/playerid/{discord_id}'.format(ip=ge.API_IP, discord_id=ID)).json()['ID']
        lvl = int(requests.get('http://{ip}/users/level/{player_id}'.format(ip=ge.API_IP, player_id=PlayerID)).text)
        xp = int(requests.get('http://{ip}/users/xp/{player_id}'.format(ip=ge.API_IP, player_id=PlayerID)).text)
        palier = lvlPalier(lvl)
        if xp >= palier:
            requests.put('http://{ip}/users/level/{player_id}/{nb}'.format(ip=ge.API_IP, player_id=PlayerID, nb=1), headers=headers)
            desc = ":tada: {1} a atteint le niveau **{0}**".format(lvl+1, Nom)
            title = "Level UP"
            msg = discord.Embed(title = title, color= 6466585, description = desc)
            msg.set_thumbnail(url=message.author.avatar_url)
            await message.channel.send(embed = msg)

        lvl2 = int(requests.get('http://{ip}/users/level/{player_id}'.format(ip=ge.API_IP, player_id=PlayerID)).text)
        if lvl == 0 and lvl2 == 1:
            await ge.addrole(member, "Joueurs")
            await ge.removerole(member, "Nouveau")
        return True
    except:
        checkInfo(ID)


async def checklevelvocal(member):
    ID = member.id
    Nom = member.name
    channel_vocal = member.guild.get_channel(507679074362064916)
    try:
        PlayerID = requests.get('http://{ip}/users/playerid/{discord_id}'.format(ip=ge.API_IP, discord_id=ID)).json()['ID']
        lvl = int(requests.get('http://{ip}/users/level/{player_id}'.format(ip=ge.API_IP, player_id=PlayerID)).text)
        xp = int(requests.get('http://{ip}/users/xp/{player_id}'.format(ip=ge.API_IP, player_id=PlayerID)).text)
        palier = lvlPalier(lvl)
        if xp >= palier:
            requests.put('http://{ip}/users/level/{player_id}/{nb}'.format(ip=ge.API_IP, player_id=PlayerID, nb=1), headers=headers)
            desc = ":tada: {1} a atteint le niveau **{0}**".format(lvl+1, Nom)
            title = "Level UP"
            msg = discord.Embed(title = title, color= 6466585, description = desc)
            msg.set_thumbnail(url=member.avatar_url)
            await channel_vocal.send(embed = msg)

        lvl2 = int(requests.get('http://{ip}/users/level/{player_id}'.format(ip=ge.API_IP, player_id=PlayerID)).text)
        if lvl == 0 and lvl2 == 1:
            await ge.addrole(member, "Joueurs")
            await ge.removerole(member, "Nouveau")
        return True
    except:
        checkInfo(ID)


def checkInfo(ID):
    req = requests.get('http://{ip}/users/playerid/{discord_id}'.format(ip=ge.API_IP, discord_id=ID)).json()
    if req['error'] == 404:
        r = requests.post('http://{ip}/users/create/?discord_id={discord_id}'.format(ip=ge.API_IP, discord_id=ID), headers=headers)
        return False
    return True
