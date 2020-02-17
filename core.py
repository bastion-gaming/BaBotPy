import discord
from discord.ext import commands
from discord.ext.commands import Bot
import datetime as dt
from datetime import datetime
import gg_lib as gg
from DB import SQLite as sql
from core import stats as stat, level as lvl, welcome as wel, gestion as ge, utils
from gems import gemsFonctions as GF
from multimedia import notification as notif
import time

# initialisation des variables.
DEFAUT_PREFIX = "!"

VERSION = open("core/version.txt").read().replace("\n", "")
TOKEN = open("token/token.txt", "r").read().replace("\n", "")
PREFIX = open("core/prefix.txt", "r").read().replace("\n", "")
client = commands.Bot(command_prefix = "{0}".format(PREFIX))
NONE = open("help/cogs.txt", "w")
NONE = open("help/help.txt", "w")

on_vocal = {}
jour = dt.date.today()

#####################################################

client.remove_command("help")

# Au démarrage du Bot.
@client.event
async def on_ready():
    global GGconnect
    print('Connecté avec le nom : {0.user}'.format(client))
    print('PREFIX = '+str(PREFIX))
    print('\nBastionBot '+VERSION)
    GF.setglobalguild(client.get_guild(utils.ServIDmoji))
    activity = discord.Activity(type=discord.ActivityType.playing, name="◀ bastion-gaming.fr ▶")
    await client.change_presence(status=discord.Status.online, activity=activity)
    print(sql.init())
    flag = sql.checkField()
    if flag == 0:
        print("SQL >> Aucun champ n'a été ajouté, supprimé ou modifié.")
    elif "add" in flag:
        print("SQL >> Un ou plusieurs champs ont été ajoutés à la DB.")
    elif "sup" in flag:
        print("SQL >> Un ou plusieurs champs ont été supprimés de la DB.")
    elif "type" in flag:
        print("SQL >> Un ou plusieurs type ont été modifié sur la DB.")
    print('------\n')
    GGconnect = ge.ZMQ()
    await notif.load(client)

####################### Commande help.py #######################

client.load_extension('help.help')

################### Core ############################

client.load_extension('core.utils')

################### Welcome #################################
@client.event
async def on_guild_join(guild):
    if guild.system_channel != None:
        systemchannel = guild.system_channel
    else:
        systemchannel = 0
    param = dict()
    param["IDGuild"] = guild.id
    ge.socket.send_string(gg.std_send_command("NewServer", guild.id, ge.name_pl, param))
    GF.msg_recv()
    await systemchannel.send('Bonjour {}!'.format(guild.name))


@client.event
async def on_member_join(member):
    guild = client.get_guild(member.guild.id)
    if guild.system_channel != None:
        systemchannel = guild.system_channel
    else:
        systemchannel = 0
    await wel.memberjoin(member, systemchannel)


@client.event
async def on_member_remove(member):
    guild = client.get_guild(member.guild.id)
    if guild.system_channel != None:
        systemchannel = guild.system_channel
    else:
        systemchannel = 0
    await systemchannel.send(wel.memberremove(member))


@client.event
async def on_voice_state_update(member, before, after):
    ID = member.id
    guild = client.get_guild(member.guild.id)
    if guild.id == wel.idBASTION:
        if guild.afk_channel != None:
            afkchannel = guild.afk_channel.id
        else:
            afkchannel = 0
        if after.channel != None and not (member.name in on_vocal) and after.channel.id != afkchannel:
            on_vocal[member.name] = time.time()
        elif (after.channel == None or after.channel.id == afkchannel) and member.name in on_vocal :
            time_on_vocal = round((time.time() - on_vocal[member.name])/60)
            print('{} as passé {} minutes en vocal !'.format(member.name, time_on_vocal))
            balXP = sql.valueAt(ID, "xp", "bastion")
            if balXP != 0:
                balXP = int(balXP[0])
            XP = balXP + int(time_on_vocal)
            sql.updateField(ID, "xp", XP, "bastion")
            await lvl.checklevelvocal(member)
            del on_vocal[member.name]


####################### Stat ####################################

@client.event
async def on_message(message):
    if not (message.author.bot or message.content.startswith(PREFIX)) :
        if message.guild.id == wel.idBASTION:
            if message.channel.id != wel.idchannel_botplay and message.channel.id != wel.idchannel_nsfw and message.channel.category_id != wel.idcategory_admin:
                await stat.countMsg(message)
                await lvl.checklevel(message)
                await client.process_commands(message)
        else:
            await client.process_commands(message)
    else:
        if GGconnect:
            await lvl.GGchecklevel(message)
        await client.process_commands(message)

####################### Commande stats.py #######################

client.load_extension('core.stats')

####################### Commande roles.py #######################

client.load_extension('core.roles')

####################### Commande level.py #######################

client.load_extension('core.level')

###################### Commande gestion.py #####################

client.load_extension('core.gestion')

###################### Commande notification.py ################

client.load_extension('multimedia.notification')

####################### Commande gems.py #######################

# client.load_extension('gems.gemsBase')
#
# client.load_extension('gems.gemsPlay')
#
# # client.load_extension('gems.gemsGuild')
#
# client.load_extension('gems.gemsEvent')
#
# client.load_extension('gems.gemsAdmin')

###################### Commande vocal.py ########################

# client.load_extension('multimedia.vocal')

##################### Commande images.py #####################

client.load_extension('multimedia.images')

###################### Commande parrain.py ########################

client.load_extension('core.parrain')

##################### Commande kaamelott.py #####################

client.load_extension('kaamelott.kaamelott')

####################### Lancemement du bot ######################


client.run(TOKEN)
