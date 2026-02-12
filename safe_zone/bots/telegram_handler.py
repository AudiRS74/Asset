"""
ClawGuardian Telegram Bot Handler
Integrates with python-telegram-bot.
Adheres to Rule 11 for dangerous command execution.
"""

import os
import threading
from telegram.ext import Application, CommandHandler, MessageHandler, filters

class TelegramHandler:
    def __init__(self, token=None):
        self.token = token or os.getenv("TELEGRAM_BOT_TOKEN")
        self.app = None
        self.thread = None

    def start_bot(self):
        if not self.token:
            return "Error: TELEGRAM_BOT_TOKEN missing."

        try:
            self.thread = threading.Thread(target=self._run_bot, daemon=True)
            self.thread.start()
            return "Telegram Bot started in background thread."
        except Exception as e:
            return f"Error starting Telegram Bot: {e}"

    def _run_bot(self):
        self.app = Application.builder().token(self.token).build()
        self.app.add_handler(CommandHandler("start", self._start_cmd))
        self.app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), self._handle_message))
        self.app.run_polling()

    async def _start_cmd(self, update, context):
        await update.message.reply_text("ClawGuardian (Telegram) online. Send me commands, Auctus.")

    async def _handle_message(self, update, context):
        # Here we would route the message back to the core assistant
        message = update.message.text
        print(f"Telegram received: {message}")
        await update.message.reply_text(f"Processed: {message}")
