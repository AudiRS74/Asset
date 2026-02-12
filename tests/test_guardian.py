import unittest
from safe_zone.voice_handler import VoiceHandler
from safe_zone.device_manager import DeviceManager

class TestClawGuardian(unittest.TestCase):
    def test_voice_security_gating(self):
        vh = VoiceHandler()
        # Default should be locked
        self.assertFalse(vh.verified)
        self.assertFalse(vh.consent_granted)
        self.assertEqual(vh.transcribe_audio(b"test"), "ERROR: Security clearance required for voice processing.")

        # Unlock
        vh.update_security_status(True, True)
        self.assertTrue(vh.verified)
        self.assertTrue(vh.consent_granted)
        self.assertEqual(vh.transcribe_audio(b"test"), "[Simulated Transcription]")

    def test_device_manager_path(self):
        dm = DeviceManager()
        self.assertTrue(len(dm.adb_path) > 0)

if __name__ == "__main__":
    unittest.main()
