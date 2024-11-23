import logging

# Set up logging configuration
logging.basicConfig(
    filename='syswatch.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

def log_alert(message):
    logging.warning(message)

def log_monitoring_data(cpu_usage, disk_activity, health_data):
    logging.info(f"CPU Usage: {cpu_usage}, Disk Activity: {disk_activity}, Health Data: {health_data}")
