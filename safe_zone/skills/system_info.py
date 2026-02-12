import platform
import psutil

KEYWORDS = ["system info", "cpu", "memory", "specs"]

def run(prompt):
    cpu_usage = psutil.cpu_percent()
    memory = psutil.virtual_memory()
    return (
        f"📊 **System Status (Python Skill):**\n"
        f"- OS: {platform.system()} {platform.release()}\n"
        f"- CPU Usage: {cpu_usage}%\n"
        f"- Memory: {memory.percent}% used ({memory.available // (1024**2)} MB available)"
    )
