"""
ClawGuardian Device Manager
Handles automation for Android, iOS, Windows, and Linux.
Utilizes ADB for Android automation.
"""

import subprocess
import shutil

class DeviceManager:
    def __init__(self):
        # Dynamically find adb path
        self.adb_path = shutil.which("adb") or "/usr/bin/adb"

    def list_android_devices(self):
        """
        Lists connected Android devices via ADB.
        """
        if not shutil.which("adb"):
            return "Error: ADB binary not found in PATH."

        try:
            result = subprocess.run([self.adb_path, "devices"], capture_output=True, text=True)
            return result.stdout
        except Exception as e:
            return f"Error listing devices: {e}"

    def run_android_command(self, device_id, command):
        """
        Runs a shell command on a specific Android device.
        Rule 4: Requires explicit user confirmation before call.
        """
        if not shutil.which("adb"):
            return "Error: ADB binary not found in PATH."

        cmd = [self.adb_path, "-s", device_id, "shell", command]
        try:
            result = subprocess.run(cmd, capture_output=True, text=True)
            return result.stdout
        except Exception as e:
            return f"Error executing command: {e}"

if __name__ == "__main__":
    dm = DeviceManager()
    print(f"Using ADB at: {dm.adb_path}")
    print("Detected Android Devices:")
    print(dm.list_android_devices())
