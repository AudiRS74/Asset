import unittest
from safe_zone.voice_handler import VoiceHandler
from safe_zone.device_manager import DeviceManager
from safe_zone.bots.telegram_handler import TelegramHandler

class TestClawGuardian(unittest.TestCase):
    def test_voice_security_gating(self):
        vh = VoiceHandler()
        self.assertFalse(vh.verified)
        vh.update_security_status(True, True)
        self.assertTrue(vh.verified)

    def test_telegram_bot_init(self):
        th = TelegramHandler(token="test_token")
        self.assertEqual(th.token, "test_token")
        self.assertEqual(th.start_bot(), "Telegram Bot initialized and waiting for commands...")

if __name__ == "__main__":
    unittest.main()
