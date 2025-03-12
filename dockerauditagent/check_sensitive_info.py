import subprocess

def check_container_sensitives(container_id):
    """Vérifier si un conteneur contient des informations sensibles."""
    try:
        sensitive_data = []  # Liste pour stocker les données sensibles
        command = f"docker inspect {container_id}"
        result = subprocess.run(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        if result.returncode == 0:
            # Si la commande réussit, analyser les variables d'environnement
            inspect_output = result.stdout.decode()

            # Chercher des variables d'environnement contenant des informations sensibles
            sensitive_keywords = ["password", "token", "key", "auth", "secret", "credentials", "db_pass"]
            for keyword in sensitive_keywords:
                if keyword.lower() in inspect_output.lower():
                    sensitive_data.append(keyword)
            
            if sensitive_data:
                return {"container_id": container_id, "sensitive_data": sensitive_data}
            else:
                return {"container_id": container_id, "sensitive_data": "No sensitive data found"}
        else:
            # Si le conteneur ne peut pas être inspecté, ajouter l'erreur retournée
            error_message = result.stderr.decode()
            return {"container_id": container_id, "error": f"Unable to inspect container: {error_message}"}
    except Exception as e:
        return {"container_id": container_id, "error": str(e)}
