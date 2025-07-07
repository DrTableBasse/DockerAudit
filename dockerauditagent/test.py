import subprocess

def check_container_log_driver(container_id):
    """Vérifier quel log driver est utilisé pour un conteneur."""
    try:
        command = f"docker inspect {container_id}"
        result = subprocess.run(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        if result.returncode == 0:
            # Analyser la sortie de docker inspect
            inspect_output = result.stdout.decode()

            # Chercher la configuration de LogConfig et extraire le log-driver
            if '"LogConfig": {' in inspect_output:
                start = inspect_output.find('"LogConfig": {') + len('"LogConfig": {')
                end = inspect_output.find('}', start)
                log_config_str = inspect_output[start:end]
                log_driver = ""
                
                for line in log_config_str.split(","):
                    if '"Type":' in line:
                        log_driver = line.split(":")[1].strip().replace('"', "")
                        break

                # Vérification si le log driver est ce que nous attendons
                if log_driver:
                    return {"container_id": container_id, "log_driver": log_driver}
                else:
                    return {"container_id": container_id, "log_driver": "No log driver configured"}
            else:
                return {"container_id": container_id, "log_driver": "No LogConfig found"}
        else:
            # Si le conteneur ne peut pas être inspecté
            error_message = result.stderr.decode()
            return {"container_id": container_id, "error": f"Unable to inspect container: {error_message}"}
    except Exception as e:
        return {"container_id": container_id, "error": str(e)}
