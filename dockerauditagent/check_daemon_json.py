# check_daemon_json.py

import os
import json

def check_daemon_json(is_rootless):
    """
    Vérifie la présence du fichier daemon.json selon que Docker fonctionne en mode rootless ou non.
    Si rootless, il cherche dans ~/.config/docker/daemon.json.
    Sinon, il cherche dans /etc/docker/daemon.json.
    Retourne un résultat JSON avec le statut et un message.
    """
    result = {
        "check": "Daemon JSON",
        "status": None
    }

    try:
        # Vérifier si Docker fonctionne en mode rootless ou non
        if is_rootless:
            # Si rootless, chercher dans ~/.config/docker/daemon.json
            daemon_path = os.path.expanduser("~/.config/docker/daemon.json")
        else:
            # Sinon, chercher dans /etc/docker/daemon.json
            daemon_path = "/etc/docker/daemon.json"

        # Vérifier si le fichier existe
        if os.path.exists(daemon_path):
            result["status"] = True

        else:
            result["status"] = False

    except Exception as e:
        result["status"] = "error"
        result["message"] = f"Une erreur s'est produite lors de la vérification du fichier daemon.json : {str(e)}"

    return json.dumps(result, indent=4, ensure_ascii=False)
