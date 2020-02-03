import subprocess
import sys


def install(package):
    try:
        subprocess.call([sys.executable, "-m", "pip", "install", "-U", package, "--user"])
    except:
        subprocess.call([sys.executable, "-m", "pip", "install", "-U", package])


install("pip")
install("discord.py")
install("tinydb")
install("pysqlite3")
install("matplotlib")
install("ffmpeg-python")
install("youtube-dl")
install("google-api-python-client")
install("google_images_download")
