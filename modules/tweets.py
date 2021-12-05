from discord.ext import tasks
from discord.ext import commands
from discord import Webhook, RequestsWebhookAdapter
import asyncio
import aiohttp
import os
import json

class TweetObtainer(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.session = aiohttp.ClientSession()
        self.sinceID = os.getenv("sinceID")
        self.getTweets.start()

    def cog_unload(self):
        self.session.close()
        self.getTweets.cancel()
        return super().cog_unload()

    @tasks.loop(seconds=1.0)
    async def getTweets(self):
        params = {"max_results": 5, "since_id": self.sinceID}
        headers = {"Authorization": f"Bearer {os.getenv('twitterBearerToken')}"}
        postWebhook = False
        async with self.session.get("https://api.twitter.com/2/users/1438243980014235659/tweets", params=params, headers=headers) as response:
            if response.status == 200:
                respJSON = await response.json()
                if respJSON["meta"]["result_count"] > 0:
                    self.sinceID = respJSON["data"][0]["id"]
                    postWebhook = True
        if postWebhook == True:
            webhook = Webhook.from_url(os.getenv("webhookURL"), adapter=RequestsWebhookAdapter())
            webhook.send(f"https://twitter.com/fiadocsbot/status/{self.sinceID}")

def setup(bot):
    bot.add_cog(TweetObtainer(bot))