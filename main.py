import json
import subprocess
from dockerauditagent.check_rootless import check_rootless
from dockerauditagent.check_daemon_json import check_daemon_json
from dockerauditagent.check_docker_socket import check_docker_socket
from dockerauditagent.get_docker_versions import check_docker_versions
from dockerauditagent.check_container_capabilities import check_containers_capabilities
from dockerauditagent.check_image_registry import check_container_registry
from dockerauditagent.check_sensitive_info import check_container_sensitives

def get_running_container_ids():
    try:
        result = subprocess.run(["docker", "ps", "-q"], capture_output=True, text=True, check=True)
        container_ids = result.stdout.strip().splitlines()
        return container_ids
    except subprocess.CalledProcessError as e:
        print(f"Erreur lors de l'exécution de docker ps: {e}")
        return []

def main():
    # Vérifier les versions Docker locales et de la dernière version
    versions_result = check_docker_versions()
    checks_results = {"docker_versions_check": json.loads(versions_result)}

    # Vérifier si Docker fonctionne en mode rootless
    rootless_result = check_rootless()
    rootless_result_dict = json.loads(rootless_result)
    checks_results["rootless_check"] = rootless_result_dict

    # Vérification du fichier daemon.json
    daemon_result = check_daemon_json(True if rootless_result_dict["status"] == "success" else False)
    daemon_result_dict = json.loads(daemon_result)
    checks_results["daemon_json_check"] = daemon_result_dict

    # Vérification du socket Docker
    if daemon_result_dict.get("status") == "success":
        socket_result = check_docker_socket(daemon_result_dict.get("daemon_json_path"))
        checks_results["docker_socket_check"] = json.loads(socket_result)
    else:
        checks_results["docker_socket_check"] = {
            "check": "Docker Socket Exposure",
            "status": "skipped",
            "message": "La vérification de daemon.json a échoué."
        }

    # Vérification des registres privés des conteneurs
    container_registry_result = check_container_registry()
    checks_results["docker_container_registry_check"] = json.loads(container_registry_result)

    # Vérification des capacités des conteneurs
    containers_capabilities_result = check_containers_capabilities()
    checks_results["docker_container_capabilities_check"] = json.loads(containers_capabilities_result)

    # Vérification des informations sensibles dans les conteneurs
    container_ids = get_running_container_ids()
    
    sensitive_info_results = {}
    for container_id in container_ids:
        sensitive_info = check_container_sensitives(container_id)
        sensitive_info_results[container_id] = sensitive_info

    checks_results["docker_container_sensitives_check"] = sensitive_info_results

    # Convertir le dictionnaire des résultats en JSON
    result_json = json.dumps(checks_results, indent=4, ensure_ascii=False)

    # Afficher le JSON
    print(result_json)

if __name__ == "__main__":
    main()
