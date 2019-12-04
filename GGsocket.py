import socket

def get_data(command, requete):
    temp = "discord-{0}-{1}".format(command, requete)
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect(("localhost", 51111))
    s.send(temp.encode())
    r = s.recv(9999999)
    s.close()
    return r.decode()
