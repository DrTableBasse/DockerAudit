# check_rootless.py

import subprocess
import json

def check_rootless():
    """
    Vérifie si Docker fonctionne en mode rootless en utilisant la commande ps aux.
    Retourne un résultat JSON avec le statut et un message.
    """
    result = {
        "check": "Docker rootless",
        "status": None
    }
    try:
        # Exécuter la commande ps aux pour lister les processus en cours
        result_ps = subprocess.run(['ps', 'aux'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

        # Filtrer les lignes contenant "dockerd" (le processus Docker)
        docker_processes = [line for line in result_ps.stdout.splitlines() if 'dockerd' in line]

        if docker_processes:
            # Vérifier si le processus Docker est lancé par root ou un autre utilisateur
            for process in docker_processes:
                user = process.split()[0]  # Le premier champ de la ligne ps aux est l'utilisateur
                if user == 'root':
                    result["status"] = False
                
                    return json.dumps(result, indent=4, ensure_ascii=False)  # Retourner le résultat sous forme JSON
            # Si le processus est lancé par un autre utilisateur que root, Docker fonctionne en mode rootless
            result["status"] = True
            result["message"] = "Docker fonctionne en mode rootless."
        else:
            result["status"] = False
        

    except Exception as e:
        result["status"] = "error"
        result["message"] = f"Une erreur s'est produite lors de la vérification du mode rootless : {str(e)}"

    return json.dumps(result, indent=4, ensure_ascii=False)
