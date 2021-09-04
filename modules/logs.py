from typing import Union
import discord
from discord.ext import commands
import os

class Logs(commands.Cog):
    def __init__(self, bot):
        """Handling of logging events for the WWR bot

        Args:
            bot (discord.Bot): The bot provided by the Discord library
        """
        self.bot = bot

    @commands.Cog.listener()
    async def on_message_edit(self, before: discord.Message, after: discord.Message):
        if before.guild != None and before.content != after.content:
            msg = discord.Embed(title="Message edit", description=f"{before.author.mention} - {before.channel.mention} - [Jump to message]({before.jump_url})", color=0xff9900)
            msg.add_field(name="Previous message", value=before.content)
            msg.add_field(name="Edited message", value=after.content)
            await self.bot.get_channel(os.getenv("auditLogChannel")).send(embed=msg)

    @commands.Cog.listener()
    async def on_message_delete(self, message: discord.Message):
        if message.guild != None:
            msg = discord.Embed(title="Message deleted", description=f"{message.author.mention} - {message.channel.mention}", color=0xff0000)
            msg.add_field(name="Message content", value=message.content)
            await self.bot.get_channel(os.getenv("auditLogChannel")).send(embed=msg)

def setup(bot):
    bot.add_cog(Logs(bot))