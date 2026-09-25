import requests, time

def check_network(config):
    target = config["network_target"]
    try:
        start = time.time()
        r = requests.get(target, timeout=5)
        end = time.time()
        return True, (end-start)*1000
    except Exception:
        return False, None
