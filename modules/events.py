import discord
from discord.ext import commands
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
        role = self.bot.get_guild(payload.guild_id).get_role(int(os.getenv("ruleAcceptRole")))
        if payload.message_id == int(os.getenv("ruleAcceptMessage")) and role not in payload.member.roles and payload.emoji.name == "✅":
            await payload.member.add_roles(role)

    @commands.Cog.listener()
    async def on_member_join(self, member: discord.Member):
        await member.send(f"Welcome to WWR {member.mention}! Make sure you agree to the rules in <#{int(os.getenv('ruleAcceptChannel'))}> by reacting with a ✅")

def setup(bot):
    bot.add_cog(Events(bot))