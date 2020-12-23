import subprocess
import sys


def install(package):
    subprocess.call([sys.executable, "-m", "pip", "install", "-U", package])


# Base
install("pip")
install("discord.py")

# Création de graphiques
install("matplotlib")

# Base de données
install("tinydb")
install("pysqlite3")

# Média
install("ffmpeg-python")
install("youtube-dl")
install("google-api-python-client")
install("google_images_download")

# Gestion des événements
install("apscheduler")
