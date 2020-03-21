import subprocess
import sys


def install(package):
    try:
        subprocess.call([sys.executable, "-m", "pip", "install", "-U", package, "--user"])
    except:
        subprocess.call([sys.executable, "-m", "pip", "install", "-U", package])
    # subprocess.call([sys.executable, "-m", "pip", "install", "-U", package])


# Base
install("pip")
install("discord.py")

# Communication avec le serveur Get Gems
install("pyzmq")
install("PyYAML")

# Création de graphiques
install("matplotlib")

# Base de données
install("tinydb")
install("pysqlite3")

# Gestion des événements
install("apscheduler")

# Média
install("ffmpeg-python")
install("youtube-dl")
install("google-api-python-client")
install("google_images_download")

# Gestion des événements
install("apscheduler")
