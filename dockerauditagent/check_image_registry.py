import subprocess
import json
import re

# Liste des fournisseurs d'images publics connus
KNOWN_PUBLIC_REGISTRIES = [
    "docker.io",  # Docker Hub
    "gcr.io",      # Google Container Registry
    "amazonaws.com",  # Amazon ECR
    "quay.io",     # Quay.io
    "registry.gitlab.com",  # GitLab Container Registry
    "hub.docker.com",  # Docker Hub (parfois utilisé dans des configurations)
    "mcr.microsoft.com",  # Microsoft Container Registry
    "public.ecr.aws",  # AWS Public ECR
    "linuxserver.io",  # LinuxServer.io
    "acr.io",  # Azure Container Registry
    "artifactory.com",  # JFrog Artifactory
    "docker.pkg.github.com",  # GitHub Package Registry
    "harbor.io",  # Harbor Registry
    "cnsupercloud.com",  # SuperCloud Registry
    "oci.example.com",  # Exemple de registre OCI
    "example-registry.com"  # Exemple de registre privé
]

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

def get_container_image(container_id):
    """Obtenir l'image utilisée par le conteneur"""
    try:
        result = subprocess.run(f"docker inspect --format '{{{{.Config.Image}}}}' {container_id}", shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        if result.returncode == 0:
            image = result.stdout.decode().strip()
            return image
        else:
            return None
    except Exception as e:
        print(f"Error while getting container image for {container_id}: {e}")
        return None

def is_private_registry(image):
    """Vérifier si l'image provient d'un registre privé basé sur des fournisseurs connus"""
    # Nous vérifions si l'image contient un des registres publics connus
    for registry in KNOWN_PUBLIC_REGISTRIES:
        if registry in image:
            return False  # Si on trouve un registre connu, ce n'est pas privé
    return True  # Si aucun registre connu n'est trouvé, on considère que c'est privé

def check_container_registry():
    """Vérifier si les conteneurs utilisent des registres privés"""
    containers = get_running_containers()

    if not containers:
        return json.dumps({"message": "No running containers found."}, indent=4, ensure_ascii=False)

    checks_results = {}

    for container_id in containers:
        container_name = get_container_name(container_id)  # Obtenir le nom du conteneur
        if container_name:
            container_running = get_container_state(container_id)  # Vérifier si le conteneur est démarré ou non
            
            # Vérification si l'image provient d'un registre privé
            container_image = get_container_image(container_id)
            is_private = is_private_registry(container_image) if container_image else False
            
            if container_running:
                checks_results[container_id] = {
                    "check": "Docker Container Registry",
                    "status": "success",
                    "container_name": container_name,
                    "running": "started",
                    "uses_private_registry": is_private,
                    "registry_type": "Public" if is_private else "Private"
                }
            else:
                checks_results[container_id] = {
                    "check": "Docker Container Registry",
                    "status": "failure",
                    "container_name": container_name,
                    "running": "stopped",
                    "message": "Container is not running."
                }
        else:
            checks_results[container_id] = {
                "check": "Docker Container Registry",
                "status": "failure",
                "message": "Failed to get container name."
            }

    # Convertir les résultats en JSON
    result_json = json.dumps(checks_results, indent=4, ensure_ascii=False)
    return result_json
