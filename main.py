import json, platform, getpass, sys, time, logging
from monitor import cpu, memory, disk, process, network, service

# Load config
with open("config.json") as f:
    config = json.load(f)

# Logging setup
logging.basicConfig(filename="logs/health.log",
                    level=logging.INFO,
                    format="%(asctime)s - %(message)s")

def system_info():
    print("===== SYSTEM INFORMATION =====")
    print("Hostname:", platform.node())
    print("OS:", platform.system(), platform.release())
    print("Kernel:", platform.version())
    print("User:", getpass.getuser())
    print("Python:", sys.version.split()[0])
    uptime = time.time() - sys.boot_time()
    print("Uptime:", time.strftime("%H:%M:%S", time.gmtime(uptime)))

def full_report():
    print("\n========================================")
    print("          SERVER HEALTH REPORT")
    print("========================================")

    usage, cpu_status = cpu.check_cpu(config)
    print(f"CPU Usage: {usage}% - {cpu_status}")
    logging.info(f"CPU: {usage}% - {cpu_status}")

    mem, mem_status = memory.check_memory(config)
    print(f"Memory Usage: {mem.percent}% - {mem_status}")
    logging.info(f"Memory: {mem.percent}% - {mem_status}")

    dsk, disk_status = disk.check_disk(config)
    print(f"Disk Usage: {dsk.percent}% - {disk_status}")
    logging.info(f"Disk: {dsk.percent}% - {disk_status}")

    net_ok, resp = network.check_network(config)
    if net_ok:
        print(f"Network: ONLINE ({resp:.0f} ms)")
        logging.info(f"Network: ONLINE {resp:.0f} ms")
    else:
        print("Network: OFFLINE")
        logging.info("Network: OFFLINE")

    svc_ok = service.check_service("nginx")
    print("Service nginx:", "ACTIVE" if svc_ok else "INACTIVE")
    logging.info(f"nginx: {'ACTIVE' if svc_ok else 'INACTIVE'}")

    # Overall status
    statuses = [cpu_status, mem_status, disk_status]
    if "CRITICAL" in statuses:
        overall = "CRITICAL"
    elif "WARNING" in statuses:
        overall = "WARNING"
    else:
        overall = "NORMAL"

    print("========================================")
    print("OVERALL STATUS:", overall)
    print("========================================")

def main():
    while True:
        print("\n========================================")
        print("        SERVER HEALTH MONITOR")
        print("========================================")
        print("1. System Information")
        print("2. CPU Usage")
        print("3. Memory Usage")
        print("4. Disk Usage")
        print("5. Process Check")
        print("6. Network Check")
        print("7. Service Check")
        print("8. Full Health Report")
        print("9. View Logs")
        print("10. Exit")

        choice = input("Enter choice: ")

        if choice == "1":
            system_info()
        elif choice == "2":
            usage, status = cpu.check_cpu(config)
            print(f"CPU Usage: {usage}% - {status}")
        elif choice == "3":
            mem, status = memory.check_memory(config)
            print(f"Memory Usage: {mem.percent}% - {status}")
        elif choice == "4":
            dsk, status = disk.check_disk(config)
            print(f"Disk Usage: {dsk.percent}% - {status}")
        elif choice == "5":
            name = input("Enter process name: ")
            ok, pid = process.check_process(name)
            print(f"Process {name}: {'RUNNING (PID '+str(pid)+')' if ok else 'NOT RUNNING'}")
        elif choice == "6":
            net_ok, resp = network.check_network(config)
            print("Network:", "ONLINE" if net_ok else "OFFLINE")
        elif choice == "7":
            name = input("Enter service name: ")
            ok = service.check_service(name)
            print(f"Service {name}: {'ACTIVE' if ok else 'INACTIVE'}")
        elif choice == "8":
            full_report()
        elif choice == "9":
            with open("logs/health.log") as f:
                print(f.read())
        elif choice == "10":
            break
        else:
            print("Invalid choice!")

if __name__ == "__main__":
    main()
