import os, sys
from discord.utils import get
from core import file


# CONFIGURATION
if not file.exist(f"{os.path.realpath(os.path.dirname(__file__))}/../config.json"):
    sys.exit("'config.json' n'a pas été trouvé! Veuillez l'ajouter et réessayer.")
else:
    CONFIG = file.json_read('config.json')
    VERSION = CONFIG['version']
    PREFIX = CONFIG['prefix']
    SECRET_KEY = CONFIG['api']['key']
    API_IP = CONFIG['api']['ip']
    TOKEN = CONFIG['token']



##### Initialisation du fichier cache #####
cache_folder = "cache/"
cache_file = f"{cache_folder}cache.json"
CACHE_TEMPLATE = {}

if (not file.exist(cache_folder)):
    file.createdir(cache_folder)

if (not file.exist(cache_file)):
    file.create(cache_file)
    file.json_write(cache_file, CACHE_TEMPLATE)
    
CACHE = file.json_read(cache_file)



admin = 0
Inquisiteur = 1
Joueurs = 2
Vasseaux = 3
rolesID = [
    [417451897729843223],
    [417451897729843223, 417451604141277185],
    [417451897729843223, 417451604141277185, 677534823694336001, 423606460908306433]
]
guildID = [
    417445502641111051, # Bastion
    129364058901053440, # TopazDev
    478003352551030796 # Test
]
idBaBot = 790899501845053461

PREFIX_LIST = ["!", "/", "*", "-", "§", "?"]




class bcolors:
    end = '\033[0m'
    black = '\033[30m'
    white = '\033[37m'
    red = '\033[31m'
    green = '\033[32m'
    yellow = '\033[33m'
    blue = '\033[34m'
    purple = '\033[35m'
    lightblue = '\033[36m'
    OK = '\033[92m' #GREEN
    WARNING = '\033[93m' #YELLOW
    FAIL = '\033[91m' #RED
    RESET = '\033[0m' #RESET COLOR



def permission(ctx, grade):
    roles = ctx.author.roles
    for role in roles :
        if role.id in rolesID[grade] or (ctx.guild.id in guildID and role.permissions.administrator):
            return True
    return False



def nom_ID(nom):
    """Convertis un nom en ID discord """
    if len(nom) == 21:
        ID = int(nom[2:20])
    elif len(nom) == 22:
        ID = int(nom[3:21])
    elif len(nom) == 18:
        ID = int(nom)
    else:
        ID = -1
    return(ID)



async def addrole(member, role):
    setrole = get(member.guild.roles, name=role)
    if setrole != None:
        await member.add_roles(setrole)
    else:
        await print("Role introuvable")



async def removerole(member, role):
    setrole = get(member.guild.roles, name=role)
    if setrole != None:
        await member.remove_roles(setrole)
    else:
        await print("Role introuvable")
