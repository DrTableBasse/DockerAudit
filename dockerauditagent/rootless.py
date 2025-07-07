import subprocess
"""
Check avec la commande 'ps aux' si Docker fonctionne en mode rootless.
Se base sur cette commande pour obtenir la liste des processus et vérifier si 'dockerd' s'exécute avec un utilisateur non-root.
si il est en mode rootless, il affiche "Docker fonctionne en mode rootless."
sinon, il affiche "Docker fonctionne en mode root (avec les privilèges root)."

"""


def check_docker_rootless():
    try:
        # Exécute la commande 'ps aux' pour obtenir la liste des processus
        result = subprocess.run(['ps', 'aux'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        
        # Recherche les processus liés à Docker
        docker_processes = [line for line in result.stdout.splitlines() if 'dockerd' in line]
        
        # Vérifie si 'dockerd' s'exécute avec un utilisateur non-root
        for process in docker_processes:
            if 'root' not in process:
                print("Docker fonctionne en mode rootless.")
                return
        print("Docker fonctionne en mode root (avec les privilèges root).")
    except FileNotFoundError:
        print("Le processus 'ps' n'est pas disponible.")
    except Exception as e:
        print(f"Une erreur est survenue : {e}")

# Exemple d'utilisation
check_docker_rootless()
