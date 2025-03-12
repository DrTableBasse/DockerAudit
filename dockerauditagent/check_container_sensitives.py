import subprocess

def check_container_sensitives(container_id):
    """Vérifier si un conteneur contient des informations sensibles."""
    try:
        sensitive_data = []  # Liste pour stocker les données sensibles
        command = f"docker inspect {container_id}"
        result = subprocess.run(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        if result.returncode == 0:
            env_vars = result.stdout.decode().splitlines()
            for env_var in env_vars:
                if "password" in env_var.lower() or "secret" in env_var.lower() or "auth" in env_var.lower():
                    sensitive_data.append(env_var)

            if sensitive_data:
                return {"container_id": container_id, "sensitive_data": sensitive_data}
            else:
                return {"container_id": container_id, "sensitive_data": "No sensitive data found"}
        else:
            error_message = result.stderr.decode()
            return {"container_id": container_id, "error": f"Unable to inspect container: {error_message}"}
    except Exception as e:
        return {"container_id": container_id, "error": str(e)}
