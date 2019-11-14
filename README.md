# BaBot
Bot discord de bastion

Suite au décès de mewna notre bot, aimée de tous sauf lorsqu'elle buggait, nous sommes dans
l'obligation de créer notre propre bot pour retrouver les services dont nous avons besoin mais
aussi des nouveaux.

## Le nom

Il se nomme BaBot

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

### Module Core

**Gestion**: Gestion des permissions.

**Vote**: Pouvoir créer un vote en configurant la *Question*, les *Réponses* et le *temps du vote*.

**Stats**: Compter le nombre de message poster dans les salons en fonction du temps. C'est
utile et là au moins on est sûr qu'il nous lis pas en même temps.

**Rôles**: Ce module va se charger de gérer les rôles. C'est a dire de mettre le rôle "Joueurs" aux
nouveaux membres mais aussi pour pouvoir en une commande créer un nouveau rôle
correspondant à un jeu puis l'associer à un salon.

**Level**: Gestion des niveaux, genre tous les x mots ou x minutes en vocal on monte d'un niveaux, ça permet de quantifier la participation de chacun aux discussions. On doit se mettre d'accord sur les modalités de leveling.

**Parrain**: Système de parrainnage offrant des gems au parrain.

**Welcome**: Gère l'affiche des messages de bienvenue au nouveaux arrivant et des messages d'aurevoir.

### Module DB

**DB**: On propose que le bot n'est qu'une seule base de donnée pour stocker les niveaux des joueurs et leur quantité d'argent. Onutilise TinyDB

### Module Multimédia

**Musique**: On propose que le bot puissent lancer des vidéos Youtube au format audio.

**Images**: Fonction permettant de faire une recherche avec mots clés sur google images et de resortir une images aléatoire.

**Live Notification**: Averti dans le salon #partage du début d'un live sur la chaine Twitch Bastion et celle des partenaires/kopains

### Module Gems

**Gems Fonctions**: Partie regroupant toutes les fonctions et les items nécessaire au fonctionnement du module.

**Gems Base**: Commandes de base du module. Il permet d'afficher par exemple le marché, l'inventaire ou le système d'achat/vente.

Liste des commandes:
- begin
- tuto
- bal
- baltop
- pay
- give
- buy
- sell
- market
- inv
- forge
- trophylist
- trophy

**Gems Play**: Commandes permettant de jouer et de gagner des GEMS (l'argent du jeu).

Liste des commandes:
- daily
- bank
- gamble
- crime
- mine
- fish
- slots
- hothouse
- boxes open

**Gems Guild**: Commandes permettant la gestion des guildes.

Liste des commandes:
- guildinfo
- guildcreate
- guildsupp
- guildleave
- guildrequest
- guildadd
- guildpromote
- guilddisplacement
- convert

**Gems Event**: Commandes relative aux évènements (limité dans le temps).

Liste des commandes:
- cooking

### Module Help

**Help**: Génère un help personnalisé

### Module Kaamelott

**Citation**: Affiche des citations venant de la série Kaamelott. Ce module à été concu exclusivement par Shelll

### Module Game Asker

**Game-Asker**: l'idée serait que quand quelqu'un sur Bastion entrerait une commande en
précisant le jeu auquel il veut jouer ça les mentionne (exactement comme on fait
aujourd'hui avec les mention de rôle) et c'est d'ailleurs ce que fera le bot MAIS je voudrais en
parallèle du Bot Bastion créer un autre bot plus léger qui en se basant sur cette idée permettrait de poster un message sur les serveurs qui l'utilisent qui précise qui veut jouer et
à quoi lorsque cette commande est entrée.



# État d'avancement du développement

## Terminés

**_Core_**
- Core
- Gestion
- Vote
- Stats
- Roles
- Level
- Parrain
- Welcome

**_DB_**

**_Multimédia_**
- Images
- Live Notification

**_Gems_**
- Gems Fonctions
- Gems Base
- Gems Play
- Gems Guild
- Gems Event

**_Help_**

**_Kaamelott_**

## En cours/test

**_Module Multimédia_**
- Musique

**_Gems_**
- Gems Fight

## Non commencé

**_Game-Asker_**
