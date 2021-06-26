from discord.utils import get

API_IP = "127.0.0.1:20216"

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
    634317171496976395, # Get Gems
    417445502641111051, # Bastion
    478003352551030796, # Test
    129364058901053440  # TopazDev
]

PREFIX_LIST = ["!", "/", "*", "-", "§", "?"]


class bcolors:
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
