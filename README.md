# bot-discord
Bot discord de bastion

Suite au décès de mewna notre bot, aimée de tous sauf lorsqu'elle buggait, nous sommes dans
l'obligation de créer notre propre bot pour retrouver les services dont nous avons besoin mais
aussi des nouveaux.

## Le nom

Question triviale mais néanmoins importante, le nom du bot. On laisse libre cours aux propositions.

## La participation

A ce jour, on a déjà commencé à créer une partie du bot et on l'a donc mis sur ce GitHub.
On pense qu'il est important qu'on soit transparent dans ce qu'on fait et tous les membres sachant
coder en python sont évidemment les bienvenus pour nous aider à coder ou émettre des
critiques constructives.

# Idées sur le fonctionnement général

## Organisation

On propose une architecture "modulaire" avec un core qui se charge de lancer les différentes
parties du bot.

## Idées de module

**Core**: Il va se charger de lancer les autres modules  

**Rôles**: Ce module va se charger de gérer les rôles. C'est a dire de mettre le rôle "Joueurs" aux
nouveaux membres mais aussi pour pouvoir en une commande créer un nouveau rôle
correspondant à un jeu puis l'associer à un salon  

**Play-bot** (alias **Gems**): Partie déjà en cours à ce jour par Shell, ce module ce chargera de gérer le jeu. Il
est semblable à celui qui existait avec Mewna. Donc toutes les commandes qui permettent
d'acheter, vendre, braquer, parier etc... De toute façon Shell est en bonne voie.  

**Level** : Gestion des niveaux, genre tous les x mots on monte d'un niveaux, ça permet de
quantifier la participation de chacun aux discussions. On doit se mettre d'accord sur les
modalités de leveling.  

**DB**: On propose que le bot n'est qu'une seule base de donnée pour stocker les niveaux des
joueurs et leur quantité d'argent. On s'y connais un peu et la seule que j'ai utilisé en python
et qui était simple c'était SQLite.
Gestion de la musique: pour n'avoir qu'un seul bot qui fait tout.  

**Vote** : faire comme celui étant déjà là.  

**Stat**: Compter le nombre de message poster dans les salons en fonction du temps. C'est
utile et là au moins on est sûr qu'il nous lis pas en même temps.  

**Game-Asker**: l'idée serait que quand quelqu'un sur Bastion entrerait une commande en
précisant le jeu auquel il veut jouer ça les mentionne (exactement comme on fait
aujourd'hui avec les mention de rôle) et c'est d'ailleurs ce que fera le bot MAIS je voudrais en
parallèle du Bot Bastion créer un autre bot plus léger qui en se basant sur cette idée permettrait de poster un message sur les serveurs qui l'utilisent qui précise qui veut jouer et
à quoi lorsque cette commande est entrée.



# État d'avancement du développement

## En cours/test

Core
Rôles
Play-bot (alias Gems)
DB

## Non commencé

Level
Vote
Game-Asker

