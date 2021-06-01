from languages import general_dict_lang
import random as ran


def init():
    listL = list()
    for l in general_dict_lang:
        listL.append(l)

    print("Lang >> La liste des langues chargées "+str(listL))


def forge_msg(langue, nom_commande, liste_variables_texte = None, shuffle = False, number = -1):
    """
    Fonction permettant de créer les messages en fonction de ceux présent dans les fichiers de langues.

    Params :
    str langue : langue en format ISO 639-1 majuscule
    str nom_commande : doit correspondre au nom de la fonction dans les fichiers de langues
    list liste_variables_texte : Ensemble des elements qui seront rajouté au texte finale par exemple 'Bravo {0}, vous avez gagné {1} gems' les éléments qui vont remplacer 0 et 1 doivent être das cet ordre dans la liste.
    bool shuffle : par défaut sur false, si mis sur "true" va renvoyer au hasard les différents choix possibles pour cette fonction dans cette langue.

    Return :
    str msg_res : Message forgé sous forme de string.
    """
    GDL = general_dict_lang

    if shuffle is False:
        if number >= 0:
            list_tmp = GDL[langue][nom_commande]
            msg_tmp = list_tmp[int(number)]
        else:
            msg_tmp = GDL[langue][nom_commande]
    else :
        list_tmp = GDL[langue][nom_commande]
        msg_tmp = ran.choice(list_tmp)

    if liste_variables_texte is None:
        return msg_tmp
    else:
        i = 0
        if number >= 0:
            list_tmp = GDL[langue][nom_commande]
            msg_tmp = list_tmp[int(number)]
        else:
            msg_tmp = GDL[langue][nom_commande]
        for x in liste_variables_texte:
            msg_tmp = msg_tmp.replace("{" + str(i) + "}", str(x))
            i += 1
        return msg_tmp
