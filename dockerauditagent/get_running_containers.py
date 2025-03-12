import subprocess

def get_running_containers():
    """Retourne une liste des conteneurs Docker en cours d'exécution."""
    try:
        command = "docker ps -q"
        result = subprocess.run(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        if result.returncode == 0:
            container_ids = result.stdout.decode().splitlines()
            return container_ids
        else:
            return []
    except Exception as e:
        return []
