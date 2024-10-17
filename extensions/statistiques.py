import os
import requests
import discord
from discord import app_commands
from discord.ext import commands, tasks
from discord.ext.commands import Context
import random as r
from operator import itemgetter
import matplotlib.pyplot as plt
import datetime as dt

from core import checks, gestion as ge, level as lvl, file

headers = {'access_token': ge.SECRET_KEY}

##### Initialisation du fichier cache #####
cache_folder = "cache/"
stats_folder = "cache/stats/"
ftime = f"{stats_folder}time.json"
fco = f"{stats_folder}co.json"

if (not file.exist(cache_folder)):
    file.createdir(cache_folder)

if (not file.exist(stats_folder)):
    file.createdir(stats_folder)

if (not file.exist(fco)):
    file.create(fco)
    file.json_write(fco, {})



def fileExist(filepath):
    try:
        with open(filepath):
            pass
    except IOError:
        return False
    return True


def countCo():
    data = file.json_read(fco)
    data["co local"] += 1
    data["co total"] += 1
    file.json_write(fco, data)


def countDeco():
    data = file.json_read(fco)
    data["deco local"] += 1
    data["deco total"] += 1
    file.json_write(fco, data)


def hourCount():
    d = dt.datetime.now().hour
    nbmsg = 0
    if fileExist(ftime) is False:
        time = {"0": 0, "1": 0, "2": 0, "3": 0, "4": 0, "5": 0, "6": 0, "7": 0, "8": 0, "9": 0, "10": 0, "11": 0, "12": 0, "13": 0, "14": 0, "15": 0, "16": 0, "17": 0, "18": 0, "19": 0, "20": 0, "21": 0, "22": 0, "23": 0}
        nbmsg = requests.get('http://{ip}/infos/msg/'.format(ip=ge.API_IP)).json()
        if nbmsg == {}:
            nbmsg = 0
        else:
            nbmsg = int(nbmsg['total_message'])
        time[str(d)] = nbmsg
        file.json_write(ftime, time)
        return d
    else:
        data = file.json_read(ftime)
        data[str(d)] = nbmsg
        file.json_write(ftime, data)
    print("time.json modifié")




class Statistiques(commands.Cog, name="statistiques"):

    def __init__(self, bot):
        self.bot = bot
        self.hour = dt.datetime.now().hour
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
                f = file.open_read(ftime)
                connexion = file.json_read(fco)
                total_heure = file.json_read(ftime)
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
                file.json_write(fco, connexion)
                date = file.json_read("cache/stats/log-{}.json".format(str(dt.date.today())[:7]))
                if date != False:
                    date[str(dt.date.today()-dt.timedelta(days = 1))] = nouveau_jour
                else:
                    date = {}
                    date[str(dt.date.today()-dt.timedelta(days = 1))] = nouveau_jour
                file.json_write("cache/stats/log-{}.json".format(str(dt.date.today())[:7]), date)
                self.day = dt.date.today()

            hourCount()
            self.hour = dt.datetime.now().hour
    

    @commands.hybrid_group(name="statistiques")
    async def statistiques(self, ctx: commands.Context):
        pass


    ################################################
    @statistiques.command(
        name="totalmsg",
        description="Donne le nombre de message posté depuis le début du bot.",
    )
    async def totalmsg(self, ctx: Context) -> None:
        """
        Donne le nombre de message posté depuis le début du bot.
        """
        msg = "Cette commande ne peut être utilisée sur ce serveur"

        if ctx.guild.id in ge.guildID:
            nbmsg = requests.get('http://{ip}/infos/msg/'.format(ip=ge.API_IP)).json()
            if nbmsg == {}:
                nbmsg = 0
            else:
                nbmsg = int(nbmsg['total_message'])
            msg = "Depuis que je suis sur ce serveur il y'a eu : {0} messages.".format(nbmsg)

        emb = discord.Embed(
            title = "Statistiques",
            color= 16777215,
            description = msg
        )
        await ctx.send(embed=emb, delete_after = 20)


    ################################################
    @statistiques.command(
        name="hourmsg",
        description="Donne le nombre de message posté dans l'heure ou entre deux heures.",
    )
    async def hourmsg(self, ctx: Context) -> None:
        """
        **[heure de début] [heure de fin]** | Donne le nombre de message posté dans l'heure ou entre deux heures.
        """
        msg = "Cette commande ne peut être utilisée sur ce serveur"

        if ctx.guild.id in ge.guildID:
            d = dt.datetime.now().hour
            if not fileExist(ftime):
                nbmsg = requests.get('http://{ip}/infos/msg/'.format(ip=ge.API_IP)).json()
                if nbmsg == {}:
                    nbmsg = 0
                else:
                    nbmsg = int(nbmsg['total_message'])
                msg = "Depuis que je suis sur ce serveur il y'a eu : {0} messages.".format(nbmsg)
                msg += "\n\nle fichier time.json est introuvable le résultat sera donc peut être faux."
            else:
                hourCount()
                t = file.json_read(ftime)
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

        emb = discord.Embed(
            title = "Statistiques",
            color= 16777215,
            description = msg
        )
        await ctx.send(embed=emb, delete_after = 20)


    ################################################
    @statistiques.command(
        name="graphheure",
        description="Affiche le graph des messages envoyés par heure.",
    )
    async def graphheure(self, ctx: Context, statue = "local", jour = "yesterday") -> None:
        """
        |local/total aaaa-mm-jj| Affiche le graph des messages envoyés par heure.
        """
        if ctx.guild.id in ge.guildID:
            if jour == "yesterday":
                jour = str(dt.date.today()-dt.timedelta(days = 1))
            logs = file.json_read("cache/stats/log-{}.json".format(jour[:7]))
            if logs == False:
                await ctx.send("la date n'est pas correcte !")
                return
            log = logs[jour]
            heures = log["msg {} heures".format(statue)]
            if os.path.isfile("cache/stats/graphheure.png"):
                os.remove('cache/stats/graphheure.png')
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
            plt.savefig("cache/stats/graphheure.png")
            await ctx.send(file=discord.File("cache/stats/graphheure.png"))
            plt.clf()
        else:
            await ctx.channel.send("commande utilisable uniquement sur le discord `Bastion`")


    ################################################
    @statistiques.command(
        name="graphjour",
        description="Affiche le graph des messages envoyés par jour.",
    )
    async def graphjour(self, ctx: Context, statue = "local", mois = "now") -> None:
        """
        |local/total aaaa-mm| Affiche le graph des messages envoyés par jour.
        """
        if ctx.guild.id in ge.guildID:
            if mois == "now":
                mois = str(dt.date.today())[:7]
            aaaa , mm = mois.split("-")
            nom_mois = dt.datetime(int(aaaa), int(mm), 1).strftime("%B")
            logs = file.json_read("cache/stats/log-{}.json".format(mois))
            if logs != False:
                ctx.send("la date n'est pas correcte !")
                pass
            if os.path.isfile("cache/stats/graphjour.png"):
                os.remove('cache/stats/graphjour.png')
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
            plt.savefig("cache/stats/graphjour.png")
            await ctx.send(file=discord.File("cache/stats/graphjour.png"))
            plt.clf()
        else:
            await ctx.channel.send("commande utilisable uniquement sur le discord `Bastion`")


    ################################################
    @statistiques.command(
        name="graphmsg",
        description="Graphique représentant le classement des membres en fonction du nombre de messages écrit.",
    )
    async def graphmsg(self, ctx: Context, r = 6) -> None:
        """
        Graphique représentant le classement des membres en fonction du nombre de messages écrit.
        """
        if ctx.guild.id in ge.guildID:
            if os.path.isfile("cache/stats/msggrapf.png"):
                os.remove('cache/stats/msggrapf.png')
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
            plt.savefig('cache/stats/msggrapf.png')
            await ctx.send(file=discord.File("cache/stats/msggrapf.png"))
            plt.clf()
            if os.path.isfile("cache/stats/msggrapf.png"):
                os.remove('cache/stats/msggrapf.png')
        else:
            await ctx.channel.send("commande utilisable uniquement sur le discord `Bastion`")


    ################################################
    @statistiques.command(
        name="graphxp",
        description="Graphique représentant le classement des membres en fonction de leur XP.",
    )
    async def graphxp(self, ctx: Context, r = 6) -> None:
        """
        Graphique représentant le classement des membres en fonction de leur XP.
        """
        if ctx.guild.id in ge.guildID:
            if os.path.isfile("cache/stats/xpgrapf.png"):
                os.remove('cache/stats/xpgrapf.png')
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
            plt.savefig('cache/stats/xpgrapf.png')
            await ctx.send(file=discord.File("cache/stats/xpgrapf.png"))
            plt.clf()
            if os.path.isfile("cache/stats/xpgrapf.png"):
                os.remove('cache/stats/xpgrapf.png')
        else:
            await ctx.channel.send("commande utilisable uniquement sur le discord `Bastion`")


    ################################################
    @statistiques.command(
        name="topxp",
        description="Classement textuel des membres du Bastion en fonction de l'XP.",
    )
    async def topxp(self, ctx: Context, n = 6) -> None:
        """
        Classement textuel des membres du Bastion en fonction de l'XP.
        """
        if ctx.guild.id in ge.guildID:
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


    ################################################
    @statistiques.command(
        name="topmsg",
        description="Classement textuel des membres du Bastion en fonction des messages postés.",
    )
    async def topmsg(self, ctx: Context, n = 6) -> None:
        """
        Classement textuel des membres du Bastion en fonction des messages postés.
        """
        if ctx.guild.id in ge.guildID:
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


    ################################################
    # @statistiques.command(
    #     name="template",
    #     description="template",
    # )
    # async def template(self, ctx: Context) -> None:
    #     """
    #     template
    #     """
    #     msg = "Cette commande ne peut être utilisée sur ce serveur"

    #     # code

    #     emb = discord.Embed(
    #         title = "Statistiques",
    #         color= 16777215,
    #         description = msg
    #     )
    #     await ctx.send(embed=emb, delete_after = 20)


################################################
async def setup(bot):
    await bot.add_cog(Statistiques(bot))