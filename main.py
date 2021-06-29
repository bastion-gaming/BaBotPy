import time
import discord
from discord.ext import commands
from discord.ext.commands import Bot

from core import level as lvl, welcome as wel, gestion as ge


# initialisation des variables.
try:
    PREFIX = open("core/prefix.txt").read().replace("\n", "")
except:
    PREFIX = "*"
VERSION = open("core/version.txt").read().replace("\n", "")
TOKEN = open("core/token.txt", "r").read().replace("\n", "")
SECRET_KEY = open("api/key.txt", "r").read().replace("\n", "")
NONE = open("core/cache/cogs.txt", "w")
intents = discord.Intents(
    messages=True,
    guilds=True,
    members=True,
    emojis=True,
    voice_states=True,
    presences=True,
    guild_messages=True,
    dm_messages=True,
    reactions=True,
    guild_reactions=True,
    dm_reactions=True
)
client = commands.Bot(command_prefix = "{p}".format(p=PREFIX), intents=intents)
on_vocal = {}
on_vocal_cam = {}
on_vocal_stream = {}

################################################

client.remove_command("help")

################################################

# Au démarrage du Bot.
@client.event
async def on_ready():
    print('Connecté avec le nom : {c.user} \nPrefix : {p} \nVersion : {v}'.format(c=client, v=VERSION, p=PREFIX))
    activity = discord.Activity(type=discord.ActivityType.playing, name="bastion-gaming.fr")
    await client.change_presence(status=discord.Status.online, activity=activity)
    print('------\n')

################### Core #######################

client.load_extension('core.commands')

client.load_extension('v2_to_v3.commands')

client.load_extension('core.parrain')

client.load_extension('core.stats')

client.load_extension('core.help')

################### Media ######################

# client.load_extension('media.vocal')

################### Welcome ####################


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
    await wel.memberremove(member, systemchannel)


################### XP #########################


@client.event
async def on_message(message):
    if not (message.author.bot or message.content.startswith(PREFIX)) :
        if message.guild.id == wel.idBASTION:
            if message.content.split()[0] not in ge.PREFIX_LIST:
                lvl.xpmsg(message)
                await lvl.checklevel(message)
    await client.process_commands(message)


@client.event
async def on_voice_state_update(member, before, after):
    ID = member.id
    guild = client.get_guild(member.guild.id)
    if guild.id == wel.idBASTION:
        if guild.afk_channel != None:
            afkchannel = guild.afk_channel.id
        else:
            afkchannel = 0

        # Voice XP
        if after.channel != None and not (member.name in on_vocal) and after.channel.id != afkchannel:
            on_vocal[member.name] = time.time()
        elif (after.channel == None or after.channel.id == afkchannel) and member.name in on_vocal :
            time_on_vocal = round((time.time() - on_vocal[member.name])/60)
            print('{} as passé {} minutes en vocal !'.format(member.name, time_on_vocal))
            lvl.addxp_voc(ID, time_on_vocal)
            await lvl.checklevelvocal(member)
            del on_vocal[member.name]

        # Cam XP
        if after.self_video and not (member.name in on_vocal_cam):
            on_vocal_cam[member.name] = time.time()
        elif (after.channel == None or not after.self_video) and member.name in on_vocal_cam :
            time_on_vocal_cam = round((time.time() - on_vocal_cam[member.name])/60)
            print('{} as passé {} minutes avec la caméra allumée !'.format(member.name, time_on_vocal_cam))
            lvl.addxp_voc(ID, time_on_vocal_cam)
            await lvl.checklevelvocal(member)
            del on_vocal_cam[member.name]

        # Stream XP
        if after.self_stream and not (member.name in on_vocal_stream):
            on_vocal_stream[member.name] = time.time()
        elif (after.channel == None or not after.self_stream) and member.name in on_vocal_stream :
            time_on_vocal_stream = round((time.time() - on_vocal_stream[member.name])/60)
            print('{} as passé {} minutes en stream !'.format(member.name, time_on_vocal_stream))
            lvl.addxp_voc(ID, time_on_vocal_stream)
            await lvl.checklevelvocal(member)
            del on_vocal_stream[member.name]


@client.event
async def on_raw_reaction_add(payload):
    if payload.guild_id == wel.idBASTION:
        ID = payload.user_id
        lvl.addxp(ID, 1)
        lvl.addreaction(ID, 1)


@client.event
async def on_raw_reaction_remove(payload):
    if payload.guild_id == wel.idBASTION:
        ID = payload.user_id
        lvl.addxp(ID, -1)
        lvl.addreaction(ID, -1)

##################### Commande kaamelott.py #####################

client.load_extension('kaamelott.kaamelott')

############## Lancemement du bot ##############

try:
    client.run(TOKEN)
except (KeyboardInterrupt, SystemExit):
    pass
