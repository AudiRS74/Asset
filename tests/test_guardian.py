import unittest
from safe_zone.voice_handler import VoiceHandler
from safe_zone.device_manager import DeviceManager
from safe_zone.bots.telegram_handler import TelegramHandler
from safe_zone.skill_loader import SkillLoader

class TestClawGuardian(unittest.TestCase):
    def test_voice_security_gating(self):
        vh = VoiceHandler()
        self.assertFalse(vh.verified)
        vh.update_security_status(True, True)
        self.assertTrue(vh.verified)

    def test_telegram_bot_init(self):
        th = TelegramHandler(token="test_token")
        self.assertEqual(th.token, "test_token")
        # Updated assertion for threaded start
        self.assertEqual(th.start_bot(), "Telegram Bot started in background thread.")

    def test_skill_loader(self):
        sl = SkillLoader()
        # Test matching keywords for system_info
        res = sl.run_skill("show me system info")
        self.assertIsNotNone(res)
        self.assertIn("System Status", res)

        # Test no match
        res_none = sl.run_skill("hello world")
        self.assertIsNone(res_none)

if __name__ == "__main__":
    unittest.main()
