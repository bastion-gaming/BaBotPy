import yaml


def std_send_command(name_c, name_p, name_pl, param_c = None):
    """
        Standardise l'émission des commandes

        Params :
        string name_c => nom commande
        string name_p => nom joueur
        string name_pl => nom plateforme
        dict param_c => les paramètres de la commande

        Return:
        string
    """
    res = dict()
    res["name_c"] = name_c
    res["name_p"] = name_p
    res["name_pl"] = name_pl

    if param_c != None :
        res["param_c"] = param_c

    return str(res)


def std_receive_command(send):
    """
        Standardise la réception des commandes

        Params :
        string send => Mettre socket.recv()

        Return :
        Dict
    """
    return yaml.safe_load(send)


# def std_log(type = "INFO", str):
#    """
#    ||| WIP |||
#    Ecrit les log
#
#    params:
#    str type => ERROR ,WARNING ,INFO
#    str str => message a affiché
#
#    return:
#    str res => [hh:mm:ss] TYPE : str
#    """


def std_answer_command(name_c, name_p, name_pl, msg = None):
    """
    Standardise la réponse du serveur au client.

    params :
    str name_c => nom de la commande
    str name_p => nom du joueur
    str name_pl => nom de la plateforme de DESTINATION
    str msg => message a afficher

    Return :
    string
    """
    res = dict()
    res["name_c"] = name_c
    res["name_p"] = name_p
    res["name_pl"] = name_pl

    if msg != None :
        res["msg"] = msg

    return str(res)
