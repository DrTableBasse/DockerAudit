import os
import json
import pwd
import subprocess

# Fonction pour vérifier la présence du fichier daemon.json
def check_daemon_json():
    result = {
        "check": "Daemon JSON",
        "status": None,
        "message": ""
    }

    try:
        # Vérification si Docker fonctionne en tant que root
        is_root = os.geteuid() == 0

        # Si Docker fonctionne en tant que root, vérifier le fichier daemon.json global
        if is_root:
            daemon_path = "/etc/docker/daemon.json"
            if os.path.exists(daemon_path):
                result["status"] = "success"
                result["message"] = f"Le fichier daemon.json existe à {daemon_path}."
            else:
                result["status"] = "failure"
                result["message"] = f"Le fichier daemon.json n'a pas été trouvé à {daemon_path}."
        else:
            # Docker fonctionne en tant que non-root, récupérer l'utilisateur
            user = get_docker_user()
            if user:
                # Si Docker fonctionne en rootless, vérifier dans ~/.config/docker/daemon.json
                rootless_daemon_path = f"/home/{user}/.config/docker/daemon.json"
                if os.path.exists(rootless_daemon_path):
                    result["status"] = "success"
                    result["message"] = f"Le fichier daemon.json existe à {rootless_daemon_path}."
                else:
                    result["status"] = "failure"
                    result["message"] = f"Le fichier daemon.json n'a pas été trouvé à {rootless_daemon_path}."
            else:
                result["status"] = "error"
                result["message"] = "Impossible de déterminer l'utilisateur Docker."

    except Exception as e:
        result["status"] = "error"
        result["message"] = f"Une erreur s'est produite: {str(e)}"
    
    return result

# Fonction pour obtenir l'utilisateur sous lequel Docker est lancé
def get_docker_user():
    try:
        # Exécuter la commande 'ps aux' pour trouver l'utilisateur exécutant le processus dockerd
        result = subprocess.run(['ps', 'aux'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        docker_processes = [line for line in result.stdout.splitlines() if 'dockerd' in line]
        
        if docker_processes:
            # Extraire l'utilisateur du processus Docker
            process_info = docker_processes[0]
            user = process_info.split()[0]  # Le nom d'utilisateur est le premier champ dans 'ps aux'
            return user
    except Exception as e:
        print(f"Erreur lors de la récupération de l'utilisateur Docker : {str(e)}")
    return None

# Fonction principale pour collecter et afficher les résultats
def main():
    result = check_daemon_json()
    
    # Convertir le résultat en JSON pour un affichage clair
    result_json = json.dumps(result, indent=4)
    print(result_json)

if __name__ == "__main__":
    main()
