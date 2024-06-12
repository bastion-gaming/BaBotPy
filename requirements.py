import subprocess
import sys


def install(package, version = None):
    if version == None or version == "":
        pv = package
    else:
        pv = "{p}=={v}".format(p=package, v=version)
    subprocess.call([sys.executable, "-m", "pip", "install", "-U", pv])


# Base
install("pip")
install("discord.py", "2.3.2")
install("requests", "2.25.1")

# Création de graphiques
# install("matplotlib", "3.4.2")

# Média
# install("ffmpeg-python", "0.2.0")
# install("youtube_dl", "2021.6.6")
# install("google-api-python-client")
# install("google_images_download")

# Gestion des événements
# install("apscheduler")
