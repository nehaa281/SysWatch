# monitor_with_progress.py - Real-time CPU monitoring with progress bars
import psutil
import time
from tqdm import tqdm

def monitor_cpu():
    # Prime the cpu_percent function to get immediate, accurate readings
    psutil.cpu_percent(interval=None, percpu=True)
    return psutil.cpu_percent(interval=0.1, percpu=True)  # Short interval for real-time updates

def display_cpu_usage():
    num_cores = psutil.cpu_count(logical=True)
    bars = [tqdm(total=100, position=i, leave=False, bar_format="{l_bar}{bar} | {n:.1f}%", desc=f"Core {i+1}") for i in range(num_cores)] 
    while True:
        try:
            # Get CPU usage for each core
            cpu_usage = monitor_cpu()

            # Update each core's progress bar
            for i, usage in enumerate(cpu_usage):
                bars[i].n = usage  # Set the progress bar to the current usage percentage
                bars[i].refresh()  # Refresh the progress bar display

        except Exception as e:
            print("Error in retrieving data:", e)
        time.sleep(0.5)  # Update every 0.5 seconds

if __name__ == "__main__":
    display_cpu_usage()

def monitor_disk():
    io_counters = psutil.disk_io_counters()
    return {
        "read_mb": io_counters.read_bytes / (1024 * 1024),
        "write_mb": io_counters.write_bytes / (1024 * 1024)
    }

def monitor_health():
    battery = psutil.sensors_battery()
    return {"battery_percent": battery.percent if battery else "N/A"}