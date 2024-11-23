import psutil
import tkinter as tk
from tkinter import ttk, font, messagebox  # Import messagebox for alerts
from monitor import monitor_cpu, monitor_disk, monitor_health
from alerts import check_alerts
from visualise import update_cpu_history, update_disk_history, plot_cpu_trend, plot_disk_trend  # Ensure correct import
from logs import log_alert, log_monitoring_data
from datetime import datetime

# Initialize the main window
root = tk.Tk()
root.title("SysWatch - System Monitoring Application")
root.geometry("700x600")
root.config(bg="#393E46")  # New background color: dark teal

# Define fonts and colors
title_font = font.Font(family="Helvetica", size=20, weight="bold")
heading_font = font.Font(family="Helvetica", size=15, weight="bold")
label_font = font.Font(family="Helvetica", size=12)
bg_color = "#393E46"  # Background color: dark teal
fg_color = "#EEEEEE"  # Text color: light gray
button_color = "#00ADB5"  # Button color: light cyan
button_hover_color = "#007A89"  # Button hover color: darker cyan

# Add a main heading
title_label = tk.Label(root, text="SysWatch - System Monitoring Application", font=title_font, bg=bg_color, fg="#FFD369")
title_label.pack(pady=20)

# Define function to format timestamps
timestamps = []
def format_timestamp():
    current_time = datetime.now().strftime("%H:%M:%S")
    timestamps.append(current_time)
    if len(timestamps) > 60:
        timestamps.pop(0)
    return current_time

# Alert tracking to avoid repeated alerts
shown_alerts = set()

# Update metrics and display alerts once
def update_metrics():
    global shown_alerts
    cpu_usage = monitor_cpu()
    disk_activity = monitor_disk()
    health = monitor_health()

    # Update CPU and Disk History for Trends
    update_cpu_history(cpu_usage)
    update_disk_history(disk_activity)

    # Check and log unique alerts
    alerts = check_alerts(cpu_usage, disk_activity, health)
    new_alerts = [alert for alert in alerts if alert not in shown_alerts]

    # Show alerts only if there are new ones
    if new_alerts:
        alert_message = "\n".join(new_alerts)
        messagebox.showinfo("SysWatch Alert", alert_message)
        for alert in new_alerts:
            shown_alerts.add(alert)
            log_alert(alert)

    # Log monitoring data
    log_monitoring_data(cpu_usage, disk_activity, health)
    root.after(1000, update_metrics)  # Schedule next update

# CPU Usage by Core Window
def show_cpu_usage():
    cpu_window = tk.Toplevel(root)
    cpu_window.title("CPU Usage by Core")
    cpu_window.geometry("400x300")
    cpu_window.config(bg=bg_color)

    cpu_usage = monitor_cpu()
    tk.Label(cpu_window, text="CPU Usage by Core", font=heading_font, bg=bg_color, fg=fg_color).pack(pady=10)

    for i, usage in enumerate(cpu_usage):
        ttk.Label(cpu_window, text=f"Core {i+1}: {usage}%", font=label_font, background=bg_color, foreground=fg_color).pack(pady=5)  
        progress = ttk.Progressbar(cpu_window, orient="horizontal", length=300, mode="determinate", maximum=100, style=f"Core{i}.Horizontal.TProgressbar") 
        progress["value"] = usage
        progress.pack()

        # Customize color of progress bar
        style = ttk.Style()
        style.configure(f"Core{i}.Horizontal.TProgressbar", background="#FF5722", troughcolor="#B0BEC5")  # Change prog>

# Disk Activity Window
def show_disk_activity():
    disk_window = tk.Toplevel(root)
    disk_window.title("Disk Activity")
    disk_window.geometry("400x300")
    disk_window.config(bg=bg_color)

    disk_activity = monitor_disk()
    tk.Label(disk_window, text="Disk Activity (MB)", font=heading_font, bg=bg_color, fg=fg_color).pack(pady=10)
    read_label = tk.Label(disk_window, text=f"Read: {disk_activity['read_mb']:.2f} MB", font=label_font, bg=bg_color,fg=fg_color)
    write_label = tk.Label(disk_window, text=f"Write: {disk_activity['write_mb']:.2f} MB", font=label_font, bg=bg_color,fg=fg_color)
    read_label.pack(pady=5)
    write_label.pack(pady=5)

# System Health Window (Battery Only)
def show_system_health():
    health_window = tk.Toplevel(root)
    health_window.title("System Health")
    health_window.geometry("400x200")
    health_window.config(bg=bg_color)

    health = monitor_health()
    tk.Label(health_window, text="System Health (Battery)", font=heading_font, bg=bg_color, fg=fg_color).pack(pady=10)
    battery_label = tk.Label(health_window, text=f"Battery: {health.get('battery_percent', 'N/A')}%", font=label_font, bg=bg_color, fg=fg_color) 
    battery_label.pack(pady=5)

# Main buttons for CPU, Disk, and Health
metrics_frame = tk.Frame(root, bg=bg_color)
metrics_frame.pack(pady=20)

cpu_button = ttk.Button(metrics_frame, text="CPU Usage by Core", command=show_cpu_usage, style="Accent.TButton")
disk_button = ttk.Button(metrics_frame, text="Disk Activity", command=show_disk_activity, style="Accent.TButton")
health_button = ttk.Button(metrics_frame, text="System Health", command=show_system_health, style="Accent.TButton")
cpu_button.grid(row=0, column=0, padx=10, pady=10)
disk_button.grid(row=0, column=1, padx=10, pady=10)
health_button.grid(row=0, column=2, padx=10, pady=10)

# Buttons for Trend Graphs
trend_button_frame = tk.Frame(root, bg=bg_color)
trend_button_frame.pack(pady=20)

cpu_trend_button = ttk.Button(trend_button_frame, text="CPU Trend", command=plot_cpu_trend, style="Accent.TButton")
disk_trend_button = ttk.Button(trend_button_frame, text="Disk Trend", command=plot_disk_trend, style="Accent.TButton")
cpu_trend_button.grid(row=0, column=0, padx=5, pady=10)
disk_trend_button.grid(row=0, column=1, padx=5, pady=10)

# Style configuration for a better look
style = ttk.Style()
style.theme_use("clam")
style.configure("Accent.TButton", background=button_color, foreground=fg_color, font=("Helvetica", 12, "bold"))
style.map("Accent.TButton", background=[("active", button_hover_color)])

# Customize progress bar style for CPU
style.configure("Core.Horizontal.TProgressbar", thickness=30)

# Start metrics update loop
update_metrics()

# Run the main event loop
root.mainloop()
