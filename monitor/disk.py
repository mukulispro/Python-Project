
import psutil

def check_disk(config):
    disk = psutil.disk_usage('/')
    usage = disk.percent
    if usage < config["disk_warning"]:
        status = "NORMAL"
    elif usage < config["disk_critical"]:
        status = "WARNING"
    else:
        status = "CRITICAL"
    return disk, status
