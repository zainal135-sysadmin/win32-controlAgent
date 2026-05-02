import psutil
import wmi
import subprocess
from datetime import datetime

def serv_stats_app_check():
    return (i for i in psutil.process_iter(['pid', 'name', 'status', 'exe']))

def serv_find_path(app_name):
    try:
        path = subprocess.check_output(f"where {app_name}", shell=True).decode()
        return path
    except subprocess.CalledProcessError:
        return 2
    
def serv_terminate_proc(pid):
    try:
        process = psutil.Process(pid)
        process.terminate()
        process.wait(timeout=4.5)
        return 0
    except psutil.AccessDenied:
        return 5
    except psutil.NoSuchProcess:
        return 2
    except Exception:
        return 1
    except psutil.TimeoutExpired:
        return 1460 
    
def serv_kill_proc(pid):
    try:
        process = psutil.Process(pid)
        process.kill()
        return 0
    except psutil.AccessDenied:
        return 5
    except Exception:
        return 1

def serv_hardware_stats():
    c = wmi.WMI()
    stats = {
        "cpu": {},
        "board": {},
        "ram": {},
        "disk": {},
        "bios": {},
        "uptime": {}
    }
    for cpu in c.Win32_Processor():
        stats["cpu"] ={
            "name": cpu.Name,
            "max_clock": cpu.MaxClockSpeed,
            "core": cpu.NumberOfCores,
            "proc": psutil.cpu_percent(interval=1)
        }
    for board in c.Win32_BaseBoard():
        stats["board"] = {
            "info": [board.Manufacturer, board.Product]
        }
    for ram in c.Win32_PhysicalMemory():
        stats["ram"] = {            
            "capacity":  int((int(ram.Capacity)) / (1024**3)),
            "speed":  ram.Speed,
            "proc": psutil.virtual_memory().percent
        }
    for disk in c.Win32_DiskDrive():
        stats["disk"] = {
            "caption":  disk.Caption,
            "size":  int(disk.Size)
        }
    for bios in c.Win32_BIOS():
        stats["bios"] = {            
            "info":  bios.Version
        }
    uptime_raw = psutil.boot_time()
    stats["uptime"] = {"time": datetime.fromtimestamp(uptime_raw).strftime("%Y-%m-%d %H:%M:%S")}
    return stats

def serv_shutdown(time: int):
    try:
        result = subprocess.run(f"shutdown /s /t {time}", shell=True, capture_output=True)
        return 0 if result.returncode == 0 else 1
    except PermissionError:
        return 5

def serv_cancel_shut():
    try:
        result = subprocess.run("shutdown /a", shell=True, capture_output=True)
        return 0 if result.returncode == 0 else 1
    except PermissionError:
        return 5

def serv_open_app(path):
    try:
        subprocess.Popen(path)
        return 0
    except FileNotFoundError:
        return 2
    except PermissionError:
        return 5
    except Exception:
        return 1
    