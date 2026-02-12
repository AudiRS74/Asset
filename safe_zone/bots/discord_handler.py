"""
ClawGuardian Discord Bot Handler
Integrates with discord.py.
Adheres to Rule 11 for dangerous command execution.
"""

import os
import threading
import discord
from discord.ext import commands
import asyncio

class DiscordHandler:
    def __init__(self, token=None):
        self.token = token or os.getenv("DISCORD_BOT_TOKEN")
        self.bot = None
        self.thread = None

    def start_bot(self):
        if not self.token:
            return "Error: DISCORD_BOT_TOKEN missing."

        try:
            self.thread = threading.Thread(target=self._run_bot, daemon=True)
            self.thread.start()
            return "Discord Bot started in background thread."
        except Exception as e:
            return f"Error starting Discord Bot: {e}"

    def _run_bot(self):
        intents = discord.Intents.default()
        intents.message_content = True
        self.bot = commands.Bot(command_prefix="/", intents=intents)

        @self.bot.event
        async def on_ready():
            print(f'Discord Bot logged in as {self.bot.user}')

        @self.bot.command()
        async def status(ctx):
            await ctx.send("ClawGuardian (Discord) is vigilant.")

        @self.bot.event
        async def on_message(message):
            if message.author == self.bot.user:
                return
            print(f"Discord received: {message.content}")
            await self.bot.process_commands(message)

        # discord.py's run() is blocking, so we need a new event loop in this thread
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        loop.run_until_complete(self.bot.start(self.token))
