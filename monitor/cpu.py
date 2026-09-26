import psutil

def check_cpu(config):
    usage = psutil.cpu_percent(interval=1)
    if usage < config["cpu_warning"]:
        status = "NORMAL"
    elif usage < config["cpu_critical"]:
        status = "WARNING"
    else:
        status = "CRITICAL"
    return usage, status
    