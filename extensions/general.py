import requests
import discord
from discord import app_commands
from discord.ext import commands
from discord.ext.commands import Context

from core import checks, gestion as ge, level


class General(commands.Cog, name="general"):
    def __init__(self, bot):
        self.bot = bot

    ################################################
    @commands.hybrid_command(
        name="help", description="Répertorie toutes les commandes que le bot a chargées."
    )
    async def help(self, ctx: Context) -> None:
        prefix = self.bot.config["prefix"]
        embed = discord.Embed(
            title="Help", description="Liste des commandes disponibles:", color=0x9C84EF
        )
        for i in self.bot.cogs:
            cog = self.bot.get_cog(i.lower())
            commands = cog.get_commands()
            data = []
            for command in commands:
                description = command.description.partition("\n")[0]
                data.append(f"{prefix}{command.name} - {description}")
            help_text = "\n".join(data)
            embed.add_field(
                name=i.capitalize(), value=f"```{help_text}```", inline=False
            )
        await ctx.send(embed=embed)

    ################################################
    @commands.hybrid_command(
        name="sync",
        description="Permet de synchroniser les commandes du bot.",
    )
    async def sync(self, ctx: Context) -> None:
        """
        Permet de synchroniser les commandes du bot.
        """
        commandsync = await ctx.bot.tree.sync(guild=ctx.guild)
        for command in commandsync:
            desc += f"\n{command.name}"
        emb = discord.Embed(
            title = "Babot",
            color= 9576994,
            description = desc
        )
        await ctx.send(embed=emb, delete_after = 20)

    ################################################
    @commands.hybrid_command(
        name="version",
        description="Permet d'avoir la version du bot.",
    )
    async def version(self, ctx: Context) -> None:
        """
        Permet d'avoir la version du bot.
        """
        emb = discord.Embed(
            title = "Babot",
            color= 9576994,
            description = f"Je suis en version {self.bot.config['version']}"
        )
        await ctx.send(embed=emb, delete_after = 20)

    ################################################
    @commands.hybrid_command(
        name="site",
        description="Affiche le lien vers le site web.",
    )
    async def site(self, ctx: Context) -> None:
        """
        Affiche le lien vers le site web.
        """
        emb = discord.Embed(
            title = "Babot",
            color= 9576994,
            description = "https://topazdev.fr/bastion-Accueil"
        )
        await ctx.send(embed=emb, delete_after = 20)

    ################################################
    @commands.hybrid_command(
        name="info",
        description="Permet d'avoir les informations d'un utilisateur",
    )
    async def info(self, ctx: Context, utilisateur: discord.User = commands.Author) -> None:
        """
        Permet d'avoir les informations d'un utilisateur
        """
        ID = utilisateur.id
        Nom = utilisateur.name

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

        if ctx.guild.id in ge.guildID:
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
            await ctx.message.delete()
            await ctx.channel.send(embed = emb)
        else:
            emb = discord.Embed(
                title = "Babot",
                color= 9576994,
                description = "Commande utilisable uniquement sur le discord Bastion!"
            )
            await ctx.send(embed=emb, delete_after = 20)

    ################################################
    @commands.hybrid_command(
        name="supp",
        description="Supprime [nombre] de message dans le channel",
    )
    @checks.is_owner()
    # @commands.check.has_permissions(administrator = True)
    async def supp(self, ctx: Context, nombre: int) -> None:
        """
        **[nombre]** | Supprime [nombre] de message dans le channel
        """
        suppMax = 40
        nb = int(nombre)
        if nb <= suppMax :
            await ctx.channel.purge(limit = nb)
            desc = '{x} messages éffacé !'.format(x=nb)
        else:
            desc = "On ne peut pas supprimer plus de {x} messages à la fois".format(x=suppMax)
        emb = discord.Embed(
            title = "Babot",
            color= 9576994,
            description = desc
        )
        await ctx.send(embed = emb, delete_after = 20)


################################################
async def setup(bot):
    await bot.add_cog(General(bot))