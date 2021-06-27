import requests
from discord.ext import commands
from discord.ext.commands import bot
import discord
from core import gestion as ge, welcome as wel, level

VERSION = open("core/version.txt").read().replace("\n", "")
SECRET_KEY = open("api/key.txt", "r").read().replace("\n", "")
headers = {'access_token': SECRET_KEY}


class Commandes(commands.Cog):

    def __init__(self, ctx):
        return(None)

    @commands.command(pass_context=True)
    async def version(self, ctx):
        """Permet d'avoir la version du bot."""
        emb = discord.Embed(title = "Version de Babot", color= 9576994, description = VERSION)
        await bot.delete_message(ctx.message)
        await ctx.channel.send(embed = emb)

    @commands.command(pass_context=True, aliases=['web', 'website'])
    async def site(self, ctx):
        """Affiche le lien vers le site web."""
        await ctx.channel.send("https://www.bastion-gaming.fr")


    @commands.command(pass_context=True, aliases=['supprimer', 'effacer', 'eff'])
    async def supp(self, ctx, nb):
        """**[nombre]** | Supprime [nombre] de message dans le channel """
        suppMax = 40
        if ge.permission(ctx, Inquisiteur):
            try :
                nb = int(nb)
                if nb <= suppMax :
                    await ctx.channel.purge(limit = nb+1)
                    desc = '{x} messages éffacé !'.format(x=nb+1)
                else:
                    desc = "On ne peut pas supprimer plus de {x} messages à la fois".format(x=suppMax)
            except ValueError:
                desc = "Commande mal remplie TOCARD"
        else :
            desc = "Tu ne remplis pas les conditions, tu fais partie de la plèbe !"
        msg = discord.Embed(title = "Message de Babot", color= 9576994, description = desc)
        await ctx.send(embed = msg, delete_after = 20)

    @commands.command(pass_context=True, aliases=['infos', 'inf'])
    async def info(self, ctx, Nom = None):
        """
        Permet d'avoir les informations d'un utilisateur
        """
        if Nom == None:
            ID = ctx.author.id
            Nom = ctx.author.name
        else:
            ID = ge.nom_ID(Nom)

        if ID != -1:
            if not level.checkInfo(ID):
                member = ctx.guild.get_member(int(ID))
                await ge.addrole(member, "Nouveau")
            PlayerID = requests.get('http://{ip}/users/playerid/{discord_id}'.format(ip=ge.API_IP, discord_id=ID)).json()['ID']
            user = requests.get('http://{ip}/users/{player_id}'.format(ip=ge.API_IP, player_id=PlayerID)).json()
            lvl = int(user['level'])
            xp = int(user['xp'])
            nbmsg = int(user['nbmsg'])
            reaction = int(user['nbreaction'])
            msg = "**Utilisateur:** {}".format(Nom)
            emb = discord.Embed(title = "Informations", color= 13752280, description = msg)

            if ctx.guild.id == wel.idBASTION:
                # Niveaux part
                msg = ""
                palier = level.lvlPalier(lvl)
                msg += "XP: `{0}/{1}`\n".format(xp, palier)
                msg += "Messages: `{0}`\n".format(nbmsg)
                msg += "Réactions: `{0}`\n".format(reaction)
                emb.add_field(name="**_Niveau_ : {0}**".format(lvl), value=msg, inline=False)

                # Parrainage
                P = user['godparent']
                F_li = requests.get('http://{ip}/users/godchilds/{player_id}'.format(ip=ge.API_IP, player_id=PlayerID)).json()
                nbF = int(requests.get('http://{ip}/users/godchilds/count/{player_id}'.format(ip=ge.API_IP, player_id=PlayerID)).text)
                msg = ""
                if P != 0:
                    msg += "\nParrain: <@{0}>".format(requests.get('http://{ip}/users/{player_id}'.format(ip=ge.API_IP, player_id=P)).json()['discord_id'])
                else :
                    msg += "\nParain: `None`"

                if nbF != 0:
                    if nbF > 1:
                        sV = "s"
                    else:
                        sV = ""
                    msg += "\nFilleul{1} `x{0}`:".format(nbF, sV)
                    for one in F_li:
                        msg += "\n<@{0}>".format(one['discord_id'])

                emb.add_field(name="**_Parrainage_**", value=msg, inline=False)
                await ctx.channel.send(embed = emb)
            else:
                await ctx.channel.send("Commande utilisable uniquement sur le discord Bastion!")
        else:
            msg = "Le nom que vous m'avez donné n'existe pas !"
            await ctx.channel.send(msg)


class SecretCommandes(commands.Cog):

    def __init__(self, ctx):
        return(None)

    @commands.command(pass_context=True)
    async def revive(self, ctx):
        await ctx.channel.send(f"Comme un phénix, <@{wel.idBaBot}> renait de ses cendres")


def setup(bot):
    bot.add_cog(Commandes(bot))
    bot.add_cog(SecretCommandes(bot))
    open("core/cache/cogs.txt", "a").write("Commandes\n")
