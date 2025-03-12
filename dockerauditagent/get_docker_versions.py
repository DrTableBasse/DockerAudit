# get_docker_versions.py

import subprocess
import requests
from bs4 import BeautifulSoup
import json

def get_local_docker_version():
    """
    Récupère la version Docker locale installée.
    """
    try:
        result = subprocess.run("docker --version", shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        if result.returncode == 0:
            version_info = result.stdout.decode().strip()
            return version_info.split()[2].strip(',')
        else:
            return None
    except Exception as e:
        print(f"Une erreur s'est produite lors de la récupération de la version locale de Docker : {e}")
        return None

def get_latest_docker_version():
    """
    Récupère la dernière version stable de Docker depuis le site officiel.
    """
    try:
        url = "https://docs.docker.com/engine/release-notes/"
        response = requests.get(url)
        response.raise_for_status()  # Vérifie si la requête est réussie
        soup = BeautifulSoup(response.text, "html.parser")
        
        # Recherche de la version en fonction de la structure actuelle de la page
        version_heading = soup.find("h3")
        if version_heading:
            version = version_heading.get_text(strip=True).split(" ")[-1]
            return version
        else:
            print("Impossible de trouver la version sur la page.")
            return None
    except requests.exceptions.RequestException as e:
        print(f"Erreur lors de la récupération de la version : {e}")
        return None

def check_docker_versions():
    """
    Vérifie les versions de Docker locales et les compare avec la dernière version disponible.
    """
    local_version = get_local_docker_version()
    latest_version = get_latest_docker_version()

    result = {
        "docker_versions_check": {
            "check": "Docker Version Check",
            "local_version": local_version if local_version else "Non trouvé"
        }
    }

    return json.dumps(result, indent=4, ensure_ascii=False)
