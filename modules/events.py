import discord
from discord.ext import commands
import asyncio
import os

class Events(commands.Cog):
    def __init__(self, bot):
        """Handling of events for the WWR bot

        Args:
            bot (discord.Bot): The bot provided by the Discord library
        """
        self.bot = bot

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload: discord.raw_models.RawReactionActionEvent):
        if payload.message_id == int(os.getenv("ruleAcceptMessage")) and payload.emoji.name == "✅":
            await payload.member.add_roles(self.bot.get_guild(payload.guild_id).get_role(int(os.getenv("ruleAcceptRole"))))


def setup(bot):
    bot.add_cog(Events(bot))