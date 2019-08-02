import discord
import random as r
import time as t

def supp(ctx,nb):
	"""suprime [nombre] de message dans le channel """
	if permission(ctx):
		try :
			nb = int(nb)
			if nb <= 20 :
				await ctx.channel.purge(limit =nb)
				msg ='{0} messages on été éffacé !'.format(nb)
			else:
				msg = "on ne peut pas supprimer plus de 20 message à la fois"
		except ValueError:
			msg = "commande mal remplis"
		return(ctx.channel.send(msg))



def permission(ctx):
	perm = 0
	roles = ctx.author.roles
	for role in roles :
		if role.permissions.value > 2000000000 :
			perm = 1
			break
	if perm == 1 :
		return(True)
	else :
		return(False)

