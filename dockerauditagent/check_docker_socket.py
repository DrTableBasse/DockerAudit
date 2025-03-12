# check_docker_socket.py

import json
import os

def check_docker_socket(daemon_json_path):
    result = {
        "check": "Docker Socket Exposure",
        "status": "failure",
        "message": "Aucun socket Docker exposé."
    }

    # Vérifier si le fichier daemon.json existe
    if os.path.exists(daemon_json_path):
        try:
            # Ouvrir et lire le fichier daemon.json
            with open(daemon_json_path, 'r') as f:
                daemon_data = json.load(f)

            # Vérifier si la clé 'hosts' existe dans daemon.json
            hosts = daemon_data.get('hosts', [])
            
            if hosts:
                # Vérifier si un socket TCP est exposé
                if any(host.startswith("tcp://") for host in hosts):
                    tcp_hosts = [host for host in hosts if host.startswith("tcp://")]
                    result = {
                        "check": "Docker Socket Exposure",
                        "status": "success",
                        "message": "Le socket Docker est exposé sur TCP.",
                        "details": {
                            "tcp_hosts": tcp_hosts
                        }
                    }
                else:
                    result["message"] = "Le socket Docker est configuré, mais il n'est ni en TCP ni en UNIX."

            else:
                result["message"] = "Aucun socket Docker n'est configuré dans daemon.json."
        
        except Exception as e:
            result["status"] = "failure"
            result["message"] = f"Erreur lors de la lecture du fichier daemon.json: {str(e)}"

    else:
        result["status"] = "failure"
        result["message"] = f"Le fichier daemon.json n'existe pas à l'emplacement : {daemon_json_path}"

    # Retourner le résultat sous forme de JSON
    return json.dumps(result, ensure_ascii=False, indent=4)
