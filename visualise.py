import matplotlib.pyplot as plt
from datetime import datetime, timezone, timedelta

# Define IST timezone (UTC + 5:30)
IST = timezone(timedelta(hours=5, minutes=30))

cpu_history = []
disk_history = []
timestamps = []

def update_cpu_history(cpu_usage):
    current_time = datetime.now(IST).strftime("%H:%M:%S")  # Current time in IST
    timestamps.append(current_time)  # Add current timestamp

    # Ensure that history lists don't grow too large
    if len(timestamps) > 60:
        timestamps.pop(0)

    cpu_history.append(cpu_usage)  # Add CPU usage data for this timestamp
    if len(cpu_history) > 60:
        cpu_history.pop(0)

def plot_cpu_trend():
    if len(timestamps) == len(cpu_history):  # Ensure data is aligned
        plt.figure(figsize=(10, 5))  # Make the plot more readable
        for i in range(len(cpu_history[0])):  # Loop through each core
            core_data = [core[i] for core in cpu_history]  # Get data for the i-th core
            plt.plot(timestamps, core_data, label=f"Core {i+1}")

        plt.title("CPU Usage Trend")
        plt.xlabel("Time (HH:MM:SS)")
        plt.ylabel("CPU Usage (%)")
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.legend()
        plt.show()

def update_disk_history(disk_activity):
    current_time = datetime.now(IST).strftime("%H:%M:%S")  # Current time in IST
    timestamps.append(current_time)  # Add current timestamp

    # Ensure that the history lists don't grow too large
    if len(timestamps) > 60:
        timestamps.pop(0)

    # Record total disk activity
    disk_history.append(disk_activity["read_mb"] + disk_activity["write_mb"])
    if len(disk_history) > 60:
        disk_history.pop(0)
     # Record total disk activity
    disk_history.append(disk_activity["read_mb"] + disk_activity["write_mb"])
    if len(disk_history) > 60:
        disk_history.pop(0)

def plot_disk_trend():
    if len(timestamps) == len(disk_history):  # Ensure data is aligned
        plt.figure(figsize=(10, 5))  # Make the plot more readable
        plt.plot(timestamps, disk_history, label="Disk Activity (MB)", color='green')

        plt.title("Disk Activity Trend")
        plt.xlabel("Time (HH:MM:SS)")
        plt.ylabel("Disk Activity (MB)")
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.legend()
        plt.show()