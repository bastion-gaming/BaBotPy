# coding: utf-8

import socket
import threading
from DB import SQLite as sql

tcpsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
tcpsock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
tcpsock.bind(("",51111))


while True:
    tcpsock.listen(10)
    print( "En écoute...")
    (clientsocket, (ip, port)) = tcpsock.accept()
    r = clientsocket.recv(2048)
    r = r.decode()
    r = r.split("-")
    if r[1] == "ID":
        try:
            IDi = int(r[2])
        except:
            IDi = sql.nom_ID(r[2])
        PlayerID = sql.get_PlayerID(IDi, "gems")
        msg = "PlayerID: {}".format(PlayerID)
    else:
        msg = "Fonction inconnu"
    clientsocket.send(msg.encode())
