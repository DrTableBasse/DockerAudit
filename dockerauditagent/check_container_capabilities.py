import subprocess
import json

def get_running_containers():
    """Obtenir la liste des conteneurs en cours d'exécution"""
    try:
        result = subprocess.run("docker ps -q", shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        if result.returncode == 0:
            containers = result.stdout.decode().strip().split('\n')
            return containers
        else:
            return []
    except Exception as e:
        print(f"Error while getting running containers: {e}")
        return []

def get_container_name(container_id):
    """Obtenir le nom du conteneur"""
    try:
        result = subprocess.run(f"docker inspect --format '{{{{.Name}}}}' {container_id}", shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        if result.returncode == 0:
            container_name = result.stdout.decode().strip().lstrip('/')
            return container_name
        else:
            return None
    except Exception as e:
        print(f"Error while getting container name for {container_id}: {e}")
        return None

def get_container_state(container_id):
    """Vérifier si le conteneur est démarré ou non"""
    try:
        result = subprocess.run(f"docker inspect --format '{{{{.State.Running}}}}' {container_id}", shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        if result.returncode == 0:
            state = result.stdout.decode().strip()
            return state == "true"  # Retourne True si le conteneur est en cours d'exécution
        else:
            return False
    except Exception as e:
        print(f"Error while checking container state for {container_id}: {e}")
        return False

def check_container_capabilities(container_id):
    """Vérifier les capacités du conteneur"""
    try:
        result = subprocess.run(f"docker inspect {container_id}", shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        if result.returncode == 0:
            container_info = json.loads(result.stdout.decode())
            if container_info:
                # Accéder aux capacités via le champ HostConfig.CapAdd
                capabilities = container_info[0].get("HostConfig", {}).get("CapAdd", [])
                return capabilities
            else:
                return []
        else:
            return []
    except Exception as e:
        print(f"Error while checking capabilities for container {container_id}: {e}")
        return []

def check_containers_capabilities():
    """Vérifier les capacités des conteneurs actifs"""
    containers = get_running_containers()

    if not containers:
        return json.dumps({"message": "No running containers found."}, indent=4, ensure_ascii=False)

    checks_results = {}

    for container_id in containers:
        container_name = get_container_name(container_id)  # Obtenir le nom du conteneur
        if container_name:
            # Ajouter le nom du conteneur avant les capacités
            container_running = get_container_state(container_id)  # Vérifier si le conteneur est démarré ou non
            capabilities = check_container_capabilities(container_id)
            if container_running:
                checks_results[container_id] = {
                    "container_name": container_name,
                    "check": "Docker Container Capabilities",
                    "status": True,
                    "running": "started",
                    "capabilities": capabilities
                }
            else:
                checks_results[container_id] = {
                    "container_name": container_name,
                    "check": "Docker Container Capabilities",
                    "status": False,
                    "running": "stopped",
                    "message": "Container is not running."
                }
        else:
            checks_results[container_id] = {
                "check": "Docker Container Capabilities",
                "status": "failure",
                "message": "Failed to get container name."
            }

    # Convertir les résultats en JSON
    result_json = json.dumps(checks_results, indent=4, ensure_ascii=False)
    return result_json
