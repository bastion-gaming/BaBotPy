import requests
import discord
from discord.ext import commands
from discord.ext.commands import bot
from core import welcome as wel, level as lvl, gestion as ge

SECRET_KEY = open("api/key.txt", "r").read().replace("\n", "")
headers = {'access_token': SECRET_KEY}

# ===============================================================
class Parrain(commands.Cog):

    def __init__(self, bot):
        return (None)

    @commands.command(pass_context=True)
    async def parrain(self, ctx, nom=None):
        """
        Permet d'ajouter un joueur comme parrain.
        En le faisant vous touchez un bonus et lui aussi
        """
        if ctx.guild.id == wel.idBASTION:
            ID = ctx.author.id
            if nom != None :
                ID_p = ge.nom_ID(nom)
                PlayerID = requests.get('http://{ip}/users/playerid/{discord_id}'.format(ip=ge.API_IP, discord_id=ID)).json()['ID']
                user = requests.get('http://{ip}/users/{player_id}'.format(ip=ge.API_IP, player_id=PlayerID)).json()
                PlayerID_p = requests.get('http://{ip}/users/playerid/{discord_id}'.format(ip=ge.API_IP, discord_id=ID_p)).json()['ID']
                if PlayerID_p != 0 and user['godparent'] == 0 and ID_p != ID:
                    requests.put('http://{ip}/users/{player_id}/godparent/{godparentID}'.format(ip=ge.API_IP, player_id=PlayerID, godparentID=PlayerID_p), headers=headers)
                    # print("Parrain ajouté")
                    lvl.addxp(PlayerID, 15)
                    fil_L = requests.get('http://{ip}/users/godchilds/count/{player_id}'.format(ip=ge.API_IP, player_id=PlayerID)).text
                    gain_p = 100 * int(fil_L)
                    lvl.addxp(PlayerID_p, gain_p)
                    msg = "Votre parrain a bien été ajouté ! Vous empochez 15 XP et lui {0} XP.".format(gain_p)
                else :
                    msg = "Impossible d'ajouter ce joueur comme parrain"

            await ctx.channel.send(msg)
        else:
            await ctx.channel.send("commande utilisable uniquement sur le discord `Bastion`")

    @commands.command(pass_context=True)
    async def filleul(self, ctx, nom = None):
        """
        Affiche la liste des filleuls d'un joueur
        """
        if ctx.guild.id == wel.idBASTION:
            if nom == None:
                ID = ctx.author.id
                nom = ctx.author.name
            else :
                ID = ge.nom_ID(nom)
                if ID == -1:
                    msg = "Ce joueur n'existe pas !"
                    await ctx.channel.send(msg)
                    return

            PlayerID = requests.get('http://{ip}/users/playerid/{discord_id}'.format(ip=ge.API_IP, discord_id=ID)).json()['ID']
            F_li = requests.get('http://{ip}/users/godchilds/count/{player_id}'.format(ip=ge.API_IP, player_id=PlayerID)).text
            countF = requests.get('http://{ip}/users/godchilds/count/{player_id}'.format(ip=ge.API_IP, player_id=PlayerID)).text
            if F_li != 0:
                if int(countF) > 1:
                    sV = "s"
                else:
                    sV = ""
                msg = "Filleul{1} `x{0}`:".format(countF, sV)
                for one in F_li:
                    msg += "\n<@{}>".format(one['discord_id'])
                emb = discord.Embed(title = "Informations :", color= 13752280, description = msg)
                await ctx.channel.send(embed = emb)
            else:
                msg = "Vous n'avez pas de filleul, invitez de nouveaux joueurs !"
                await ctx.channel.send(msg)
        else:
            await ctx.channel.send("commande utilisable uniquement sur le discord `Bastion`")

    @commands.command(pass_context=True)
    async def filleul_supp(self, ctx, nom):
        """
        Affiche la liste des filleuls d'un joueur
        """
        if ctx.guild.id == wel.idBASTION:
            ID_p = ctx.author.id
            ID_f = ge.nom_ID(nom)
            if ID_f == -1:
                msg = "Ce joueur n'existe pas !"
                await ctx.channel.send(msg)
                return

            PlayerID_p = requests.get('http://{ip}/users/playerid/{discord_id}'.format(ip=ge.API_IP, discord_id=ID)).json()['ID']
            PlayerID_f = requests.get('http://{ip}/users/playerid/{discord_id}'.format(ip=ge.API_IP, discord_id=ID_f)).json()['ID']
            user_f = requests.get('http://{ip}/users/{player_id}'.format(ip=ge.API_IP, player_id=PlayerID_f)).json()
            parrain = user_f['godparent']
            if parrain == 0:
                return await ctx.channel.send("Ce joueur n'a pas de parrain")
            if parrain == PlayerID_p:
                lvl.addxp(PlayerID_f, -15)
                fil_count = requests.get('http://{ip}/users/godchilds/count/{player_id}'.format(ip=ge.API_IP, player_id=PlayerID_p)).text
                gain_p = -100 * int(fil_count)
                lvl.addxp(PlayerID_p, gain_p)
                requests.put('http://{ip}/users/{player_id}/godparent/{godparentID}'.format(ip=ge.API_IP, player_id=PlayerID_f, godparentID=0), headers=headers)
                msg = "Votre filleul <@{filleul}> a bien été retiré ! Vous perdez {xp_p} XP et lui 15 XP.".format(filleul=ID_f, xp_p=-gain_p)
            else:
                msg = "Vous n'etes pas son parrain !"
            await ctx.channel.send(msg)
        else:
            await ctx.channel.send("commande utilisable uniquement sur le discord `Bastion`")


def setup(bot):
    bot.add_cog(Parrain(bot))
    open("core/cache/cogs.txt", "a").write("Parrain\n")
