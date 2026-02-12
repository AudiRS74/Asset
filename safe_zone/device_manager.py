"""
ClawGuardian Device Manager
Handles automation for Android, iOS, Windows, and Linux.
Initial implementation focuses on Android via ADB.
"""

import subprocess

class DeviceManager:
    def __init__(self):
        self.adb_path = "/opt/android-sdk/platform-tools/adb"

    def list_android_devices(self):
        """
        Lists connected Android devices via ADB.
        """
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
        # Actual execution would follow user confirmation
        cmd = [self.adb_path, "-s", device_id, "shell", command]
        try:
            result = subprocess.run(cmd, capture_output=True, text=True)
            return result.stdout
        except Exception as e:
            return f"Error executing command: {e}"

if __name__ == "__main__":
    dm = DeviceManager()
    print("Detected Android Devices:")
    print(dm.list_android_devices())
