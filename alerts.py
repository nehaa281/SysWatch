# alerts.py - Updated Alert Checking

CPU_THRESHOLD = 80
DISK_THRESHOLD = 90
TEMP_THRESHOLD = 75

def check_alerts(cpu_usage, disk_activity, health_data):
    alerts = []

    # CPU usage alert
    if any(core > CPU_THRESHOLD for core in cpu_usage):
        alerts.append("High CPU usage detected!")

    # Disk activity alert
    if disk_activity["read_mb"] > DISK_THRESHOLD or disk_activity["write_mb"] > DISK_THRESHOLD:
        alerts.append("High disk activity detected!")

    # Temperature alert (only if temperature data is available)
    temperature = health_data.get("temperature")
    if temperature and temperature != "N/A":
        try:
            temp_value = float(temperature.strip("+°C"))
            if temp_value > TEMP_THRESHOLD:
                alerts.append("High CPU temperature detected!")
        except ValueError:
            pass  # Ignore if temperature can't be converted to a float
     # Fan speed alert (optional, only if fan speed data is available)
    fan_speed = health_data.get("fan_speed")
    if fan_speed and fan_speed != "N/A" and int(fan_speed) < 1000:  # Example threshold
        alerts.append("Fan speed is too low!")

    return alerts