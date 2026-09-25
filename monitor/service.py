import subprocess

def check_service(name):
    try:
        result = subprocess.run(["systemctl", "is-active", name],
                                capture_output=True, text=True)
        return result.stdout.strip() == "active"
    except Exception:
        return False
 