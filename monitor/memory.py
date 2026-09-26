import psutil

def check_memory(config):
    mem = psutil.virtual_memory()
    usage = mem.percent
    if usage < config["memory_warning"]:
        status = "NORMAL"
    elif usage < config["memory_critical"]:
        status = "WARNING"
    else:
        status = "CRITICAL"
    return mem, status
