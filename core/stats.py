import os
import requests
import json
import discord
from discord.ext import commands, tasks
from discord.ext.commands import bot
from operator import itemgetter
import matplotlib.pyplot as plt
import datetime as dt

from core import welcome as wel, gestion as ge, level

file = "core/cache/time.json"
co = "core/cache/co.json"


def fileExist():
    try:
        with open(file):
            pass
    except IOError:
        return False
    return True


def countCo():
    t = json.load(open(co, "r"))
    t["co local"] += 1
    t["co total"] += 1
    with open(co, 'w') as f:
        f.write(json.dumps(t, indent=4))


def countDeco():
    t = json.load(open(co, "r"))
    t["deco local"] += 1
    t["deco total"] += 1
    with open(co, 'w') as f:
        f.write(json.dumps(t, indent=4))

def hourCount():
    d = dt.datetime.now().hour
    if fileExist() is False:
        t = {"0": 0, "1": 0, "2": 0, "3": 0, "4": 0, "5": 0, "6": 0, "7": 0, "8": 0, "9": 0, "10": 0, "11": 0, "12": 0, "13": 0, "14": 0, "15": 0, "16": 0, "17": 0, "18": 0, "19": 0, "20": 0, "21": 0, "22": 0, "23": 0}
        nbmsg = requests.get('http://{ip}/infos/msg/'.format(ip=ge.API_IP)).json()
        if nbmsg == {}:
            nbmsg = 0
        else:
            nbmsg = int(nbmsg['total_message'])
        t[str(d)] = nbmsg
        with open(file, 'w') as f:
            f.write(json.dumps(t, indent=4))
        return d
    else:
        with open(file, "r") as f:
            t = json.load(f)
            t[str(d)] = nbmsg
        with open(file, 'w') as f:
            f.write(json.dumps(t, indent=4))
    print("time.json modifié")


# ===============================================================
class Stats(commands.Cog):

    def __init__(self, bot):
        self.hour = dt.datetime.now().hour
        self.bot = bot
        self.day = dt.date.today()
        self.hourWrite.start()
        return(None)

    def cog_unload(self):
        self.hourWrite.cancel()

    @tasks.loop(seconds=300.0)
    async def hourWrite(self):
        """
        Va, toute les heures, écrire dans time.json le nombre total de message écrit sur le serveur.
        """
        if self.hour != dt.datetime.now().hour :
            if self.day != dt.date.today():
                msg_total = requests.get('http://{ip}/infos/msg/'.format(ip=ge.API_IP)).json()
                if msg_total == {}:
                    msg_total = 0
                else:
                    msg_total = int(msg_total['total_message'])
                local_heure = {}
                f = open(file, "r")
                connexion = json.load(open(co, "r"))
                total_heure = json.load(open(file, "r"))
                for i in range(23):
                    local_heure[str(i)] = total_heure[str(i+1)] - total_heure[str(i)]
                local_heure["23"] = msg_total - total_heure[str("23")]
                msg_jour = msg_total - total_heure["0"]
                nouveau_jour = {
                    "msg total jour" : msg_total,
                    "msg local jour" : msg_jour,
                    "msg total heures" : total_heure,
                    "msg local heures" : local_heure,
                    "co local" : connexion["co local"],
                    "co total" : connexion["co total"],
                    "deco total" : connexion["deco total"],
                    "deco local" : connexion["deco local"]
                }
                connexion["co local"] = 0
                connexion["deco local"] = 0
                with open(co, 'w') as f:
                    f.write(json.dumps(connexion, indent=4))
                try:
                    with open("core/logs/log-{}.json".format(str(dt.date.today())[:7]), 'r') as f:
                        t = json.load(f)
                        t[str(dt.date.today()-dt.timedelta(days = 1))] = nouveau_jour
                        f.close()
                except:
                    t = {}
                    t[str(dt.date.today()-dt.timedelta(days = 1))] = nouveau_jour
                with open("core/logs/log-{}.json".format(str(dt.date.today())[:7]), 'w') as f:
                    f.write(json.dumps(t, indent=4))
                self.day = dt.date.today()

            hourCount()
            self.hour = dt.datetime.now().hour

    @commands.command(pass_context=True)
    async def totalMsg(self, ctx):
        """
        Donne le nombre de message posté depuis le début du bot.
        """
        if ctx.guild.id == wel.idBASTION:
            nbmsg = requests.get('http://{ip}/infos/msg/'.format(ip=ge.API_IP)).json()
            if nbmsg == {}:
                nbmsg = 0
            else:
                nbmsg = int(nbmsg['total_message'])
            msg = "Depuis que je suis sur ce serveur il y'a eu : {0} messages.".format(nbmsg)
            await ctx.channel.send(msg)

    @commands.command(pass_context=True)
    async def hourMsg(self, ctx, ha=None, hb=None):
        """
        **[heure de début] [heure de fin]** | Donne le nombre de message posté dans l'heure ou entre deux heures.
        """
        if ctx.guild.id == wel.idBASTION:
            d = dt.datetime.now().hour
            if not fileExist():
                nbmsg = requests.get('http://{ip}/infos/msg/'.format(ip=ge.API_IP)).json()
                if nbmsg == {}:
                    nbmsg = 0
                else:
                    nbmsg = int(nbmsg['total_message'])
                msg = "Depuis que je suis sur ce serveur il y'a eu : {0} messages.".format(nbmsg)
                await ctx.channel.send(msg)
                await ctx.channel.send("le fichier time.json est introuvable le résultat sera donc peut être faux.")
            else:
                hourCount()
                with open(file, "r") as f:
                    t = json.load(f)
                if ha != None and hb != None:
                    ha = int(ha)
                    hb = int(hb)
                    if ha >= 0 and hb >= 0 and ha < 24 and hb < 24:
                        nbMsg = t[str(hb)]-t[str(ha)]
                        msg = "Entre {0}h et {1}h il y a eu {2} messages.".format(ha, hb, nbMsg)
                    else :
                        msg = "Vous avez entré une heure impossible."
                else :
                    if d != 0:
                        nbMsg = t[str(d)]-t[str(d-1)]
                    else:
                        nbMsg = t["0"]-t["23"]
                    msg = "Depuis {0}h il y'a eu: {1} messages postés.".format(d, nbMsg)
                await ctx.channel.send(msg)
        else:
            await ctx.channel.send("commande utilisable uniquement sur le discord `Bastion`")

    @commands.command(pass_context=True)
    async def graphheure(self, ctx, statue = "local", jour = "yesterday"):
        """|local/total aaaa-mm-jj| Affiche le graph des messages envoyés par heure."""
        if ctx.guild.id == wel.idBASTION:
            if jour == "yesterday":
                jour = str(dt.date.today()-dt.timedelta(days = 1))
            try :
                logs = json.load(open("core/logs/log-{}.json".format(jour[:7]), "r"))
            except FileNotFoundError :
                await ctx.send("la date n'est pas correcte !")
                return
            log = logs[jour]
            heures = log["msg {} heures".format(statue)]
            if os.path.isfile("core/cache/graphheure.png"):
                os.remove('core/cache/graphheure.png')
                print('removed old graphe file')
            x = []
            y = []
            for i in range(24):
                x.append(i)
                y.append(heures[str(i)])
            if statue == "local":
                plt.hist(x, bins = 24, weights = y)
            else :
                plt.plot(x, y, label="graph test")
                plt.fill_between(x, y[0]-100, y, color='blue', alpha=0.5)
            plt.xlabel('heures')
            plt.ylabel('messages')
            plt.title("graphique du {}".format(jour))
            plt.savefig("core/cache/graphheure.png")
            await ctx.send(file=discord.File("core/cache/graphheure.png"))
            plt.clf()
        else:
            await ctx.channel.send("commande utilisable uniquement sur le discord `Bastion`")

    @commands.command(pass_context=True)
    async def graphjour(self, ctx, statue = "local", mois = "now"):
        """|local/total aaaa-mm| Affiche le graph des messages envoyés par jour."""
        if ctx.guild.id == wel.idBASTION:
            if mois == "now":
                mois = str(dt.date.today())[:7]
            aaaa , mm = mois.split("-")
            nom_mois = dt.datetime(int(aaaa), int(mm), 1).strftime("%B")
            try :
                logs = json.load(open("core/logs/log-{}.json".format(mois), "r"))
            except ValueError :
                ctx.send("la date n'est pas correcte !")
                pass
            if os.path.isfile("core/cache/graphjour.png"):
                os.remove('core/cache/graphjour.png')
                print('removed old graphe file')
            msg = []
            jour = []
            text = "msg {} jour".format(statue)
            for i in range(1, 32):
                try :
                    if i < 10:
                        msg.append(logs["{}-0{}".format(mois, i)][text])
                    else:
                        msg.append(logs["{}-{}".format(mois, i)][text])
                    jour.append(i)
                except KeyError :
                    pass
            if statue == "local":
                plt.hist(jour, bins = len((logs)), weights = msg)
            else :
                plt.plot(jour, msg, label="graph test")
                plt.fill_between(jour, msg[0]-200, msg, color='blue', alpha=0.5)
            plt.xlabel('jour')
            plt.ylabel('messages')
            plt.title("graphique du {} au {} {}".format(jour[0], jour[len(jour)-1], nom_mois))
            plt.savefig("core/cache/graphjour.png")
            await ctx.send(file=discord.File("core/cache/graphjour.png"))
            plt.clf()
        else:
            await ctx.channel.send("commande utilisable uniquement sur le discord `Bastion`")

    @commands.command(pass_context=True, aliases=['graphmembre'])
    async def graphmsg(self, ctx, r = 6):
        """
        Graphique représentant le classement des membres en fonction du nombre de messages écrit.
        """
        if ctx.guild.id == wel.idBASTION:
            if os.path.isfile("core/cache/msggrapf.png"):
                os.remove('core/cache/msggrapf.png')
                print('removed old graphe file')
            total = requests.get('http://{ip}/infos/msg/'.format(ip=ge.API_IP)).json()
            if total == {}:
                total = 0
            else:
                total = int(total['total_message'])
            a = []
            taille = requests.get('http://{ip}/infos/nb_player/'.format(ip=ge.API_IP)).json()
            if taille == {}:
                taille = 0
            else:
                taille = int(taille['taille'])
            users = requests.get('http://{ip}/users/?skip=0&limit={max}'.format(ip=ge.API_IP, max=taille)).json()
            for user in users:
                IDi = user['discord_id']
                nbMsg = user['nbmsg']
                Name = ctx.guild.get_member(IDi).name
                a.append([nbMsg, IDi, Name])
            a.sort(reverse = True)
            richest = a[:r]
            sous_total = 0
            for i in range(r):
                sous_total += richest[i][0]
            labels = []
            sizes = []
            for i in range(r):
                try:
                    labels.append(ctx.guild.get_member(richest[i][1]).name)
                    sizes.append(richest[i][0])
                except:
                    labels.append("Utilisateur inconnu\n{}".format(richest[i][1]))
                    sizes.append(richest[i][0])
            labels.append("autre")
            sizes.append(total - sous_total)
            explode = ()
            i = 0
            while i <= r:
                if i < r:
                    explode = explode + (0,)
                else:
                    explode = explode + (0.2,)
                i += 1
            plt.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=90, explode=explode)
            plt.axis('equal')
            plt.savefig('core/cache/msggrapf.png')
            await ctx.send(file=discord.File("core/cache/msggrapf.png"))
            plt.clf()
            if os.path.isfile("core/cache/msggrapf.png"):
                os.remove('core/cache/msggrapf.png')
        else:
            await ctx.channel.send("commande utilisable uniquement sur le discord `Bastion`")

    @commands.command(pass_context=True)
    async def graphxp(self, ctx, r = 6):
        """
        Graphique représentant le classement des membres en fonction de leur XP.
        """
        if ctx.guild.id == wel.idBASTION:
            if os.path.isfile("core/cache/xpgrapf.png"):
                os.remove('core/cache/xpgrapf.png')
                print('removed old graphe file')
            total = requests.get('http://{ip}/infos/xp/'.format(ip=ge.API_IP)).json()
            if total == {}:
                total = 0
            else:
                total = int(total['total_xp'])
            a = []
            taille = requests.get('http://{ip}/infos/nb_player/'.format(ip=ge.API_IP)).json()
            if taille == {}:
                taille = 0
            else:
                taille = int(taille['taille'])
            users = requests.get('http://{ip}/users/?skip=0&limit={max}'.format(ip=ge.API_IP, max=taille)).json()
            for user in users:
                IDi = user['discord_id']
                nbMsg = user['nbmsg']
                Name = ctx.guild.get_member(IDi).name
                a.append([nbMsg, IDi, Name])
            a.sort(reverse = True)
            richest = a[:r]
            sous_total = 0
            for i in range(r):
                sous_total += richest[i][0]
            labels = []
            sizes = []
            for i in range(r):
                try:
                    labels.append(ctx.guild.get_member(richest[i][1]).name)
                    sizes.append(richest[i][0])
                except:
                    labels.append(richest[i][1])
                    sizes.append(richest[i][0])
            labels.append("autre")
            sizes.append(total - sous_total)
            explode = ()
            i = 0
            while i <= r:
                if i < r:
                    explode = explode + (0,)
                else:
                    explode = explode + (0.2,)
                i += 1
            plt.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=90, explode=explode)
            plt.axis('equal')
            plt.savefig('core/cache/xpgrapf.png')
            await ctx.send(file=discord.File("core/cache/xpgrapf.png"))
            plt.clf()
            if os.path.isfile("core/cache/xpgrapf.png"):
                os.remove('core/cache/xpgrapf.png')
        else:
            await ctx.channel.send("commande utilisable uniquement sur le discord `Bastion`")

    @commands.command(pass_context=True)
    async def topxp(self, ctx, n = 6):
        """
        Classement textuel des membres du Bastion en fonction de l'XP.
        """
        if ctx.guild.id == wel.idBASTION:
            UserList = []
            taille = requests.get('http://{ip}/infos/nb_player/'.format(ip=ge.API_IP)).json()
            if taille == {}:
                taille = 0
            else:
                taille = int(taille['taille'])
            users = requests.get('http://{ip}/users/?skip=0&limit={max}'.format(ip=ge.API_IP, max=taille)).json()
            for user in users:
                IDi = int(user['discord_id'])
                nbMsg = user['nbmsg']
                XP = user['xp']
                mylvl = user['level']
                Arrival = user['arrival'][:10]
                try:
                    Name = ctx.guild.get_member(IDi).name
                    UserList.append([IDi, XP, nbMsg, Arrival, Name, mylvl])
                except:
                    pass
            UserList = sorted(UserList, key=itemgetter(1), reverse=True)
            Titre = "Classement des membres en fonction de l'XP"
            j = 1
            desc = ""
            for one in UserList: # affichage des données trié
                if j <= n:
                    desc += "{number} |`{name}`: **{XP}** XP • Niveau **{niv}** • _{msg}_ messages postés depuis le {arrival}\n".format(number=j, name=one[4], XP=one[1], msg=one[2], arrival=one[3], niv=one[5])
                    if j % 20 == 0 and j != 0:
                        MsgEmbed = discord.Embed(title = Titre, color= 13752280, description = desc)
                        desc = ""
                        await ctx.channel.send(embed = MsgEmbed)
                j += 1
            if desc != "":
                MsgEmbed = discord.Embed(title = Titre, color= 13752280, description = desc)
                await ctx.channel.send(embed = MsgEmbed)
        else:
            await ctx.channel.send("Commande utilisable uniquement sur le discord `Bastion`")

    @commands.command(pass_context=True)
    async def topmsg(self, ctx, n = 6):
        """
        Classement textuel des membres du Bastion en fonction des messages postés.
        """
        if ctx.guild.id == wel.idBASTION:
            UserList = []
            taille = requests.get('http://{ip}/infos/nb_player/'.format(ip=ge.API_IP)).json()
            if taille == {}:
                taille = 0
            else:
                taille = int(taille['taille'])
            users = requests.get('http://{ip}/users/?skip=0&limit={max}'.format(ip=ge.API_IP, max=taille)).json()
            for user in users:
                IDi = int(user['discord_id'])
                nbMsg = user['nbmsg']
                XP = user['xp']
                mylvl = user['level']
                Arrival = user['arrival'][:10]
                try:
                    Name = ctx.guild.get_member(IDi).name
                    UserList.append([IDi, XP, nbMsg, Arrival, Name, mylvl])
                except:
                    pass
            UserList = sorted(UserList, key=itemgetter(2), reverse=True)
            Titre = "Classement des membres en fonction du nombre de messages postés"
            j = 1
            desc = ""
            for one in UserList: # affichage des données trié
                if j <= n:
                    desc += "{number} |`{name}`: **{msg}** messages postés depuis le {arrival} • _{XP}_ XP • Niveau **{niv}**\n".format(number=j, name=one[4], XP=one[1], msg=one[2], arrival=one[3], niv=one[5])
                    if j % 20 == 0 and j != 0:
                        MsgEmbed = discord.Embed(title = Titre, color= 13752280, description = desc)
                        desc = ""
                        await ctx.channel.send(embed = MsgEmbed)
                j += 1
            if desc != "":
                MsgEmbed = discord.Embed(title = Titre, color= 13752280, description = desc)
                await ctx.channel.send(embed = MsgEmbed)
        else:
            await ctx.channel.send("Commande utilisable uniquement sur le discord `Bastion`")


# ===============================================================
class StatsOld(commands.Cog):

    def __init__(self, bot):
        return(None)

    @commands.command(pass_context=True, aliases=['oldtopxp', 'oldop'])
    async def oldtop(self, ctx, n = 6):
        """
        Ancien classement textuel des membres du Bastion en fonction de l'XP.
        """
        if ctx.guild.id == wel.idBASTION:
            UserList = []
            taille = requests.get('http://{ip}/infos/nb_player/'.format(ip=ge.API_IP)).json()
            if taille == {}:
                taille = 0
            else:
                taille = int(taille['taille'])
            users = requests.get('http://{ip}/users/old/?skip=0&limit={max}'.format(ip=ge.API_IP, max=taille)).json()
            for user in users:
                IDi = int(user['discord_id'])
                XP = user['xp']
                mylvl = user['level']
                try:
                    Name = ctx.guild.get_member(IDi).name
                    UserList.append([IDi, XP, Name, mylvl])
                except:
                    pass
            UserList = sorted(UserList, key=itemgetter(1), reverse=True)
            Titre = "Classement des membres en fonction de l'XP"
            j = 1
            desc = ""
            for one in UserList: # affichage des données trié
                if j <= n:
                    desc += "{number} |`{name}`: **{XP}** XP | Niveau **{niv}**\n".format(number=j, name=one[2], XP=one[1], niv=one[3])
                    if j % 20 == 0 and j != 0:
                        MsgEmbed = discord.Embed(title = Titre, color= 13752280, description = desc)
                        desc = ""
                        await ctx.channel.send(embed = MsgEmbed)
                j += 1
            if desc != "":
                MsgEmbed = discord.Embed(title = Titre, color= 13752280, description = desc)
                await ctx.channel.send(embed = MsgEmbed)
        else:
            await ctx.channel.send("Commande utilisable uniquement sur le discord `Bastion`")


    @commands.command(pass_context=True, aliases=['infox', 'infx'])
    async def oldinfo(self, ctx, Nom = None):
        """
        Permet d'avoir les anciennes informations d'un utilisateur
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
            user = requests.get('http://{ip}/users/old/{player_id}'.format(ip=ge.API_IP, player_id=PlayerID)).json()
            lvl = int(user['level'])
            xp = int(user['xp'])
            msg = "**Utilisateur:** {}".format(Nom)
            emb = discord.Embed(title = "Informations", color= 13752280, description = msg)

            if ctx.guild.id == wel.idBASTION:
                # Niveaux part
                msg = ""
                palier = level.lvlPalier(lvl)
                msg += "XP: `{0}/{1}`\n".format(xp, palier)
                emb.add_field(name="**_Niveau_ : {0}**".format(lvl), value=msg, inline=False)
                await ctx.channel.send(embed = emb)
            else:
                await ctx.channel.send("Commande utilisable uniquement sur le discord Bastion!")
        else:
            msg = "Le nom que vous m'avez donné n'existe pas !"
            await ctx.channel.send(msg)


def setup(bot):
    bot.add_cog(Stats(bot))
    bot.add_cog(StatsOld(bot))
    open("core/cache/cogs.txt", "a").write("Stats\n")
