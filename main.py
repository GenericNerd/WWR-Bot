import logging
from discord import Intents
from discord.ext import commands
from dotenv import load_dotenv
import os
from datetime import datetime

# Create a log file and a logger object to send logs
logging.basicConfig(filename=f"{__name__}.log", level=logging.DEBUG, format="[%(asctime)s - %(levelname)s] %(message)s", datefmt="%d/%b/%Y %H:%M:%S")
logger = logging.getLogger(__name__)
logger.info("Starting WWR Bot")

# Attempt to load a .env file, if none exists, use the default settings
try:
    load_dotenv()
except BaseException:
    logger.warning(".env file could not be loaded, using default settings")

# Obtain environment variables
token = os.getenv("botToken")
release = os.getenv("release",f"debug-{datetime.utcnow().isocalendar()[1]}")
environment = os.getenv("environment","development")
prefix = os.getenv("botPrefix")

# Set startup cogs that will be loaded when the bot starts
startupCogs = ["events", "logs", "tweets"]

intents = Intents.default()
intents.members = True
intents.presences = True
intents.reactions = True
bot = commands.Bot(command_prefix=(prefix, prefix.lower()), intents=intents)
logger.info(f"Using bot prefix \"{prefix}\"")

# Attempt to load each cog
for cog in startupCogs:
    try:
        bot.load_extension(f"modules.{cog}")
        logger.info(f"{cog} loaded")
    except Exception as e:
        logger.error(f"Unable to load {cog}: {e}")

# If there is an error, put it in the log file
# @bot.event
# async def on_error(event, *args, **kwargs):
#     logger.error(f"{event=} {args=} {kwargs=}")

logger.info("Running WWR Bot")
# Run the bot with the token provided with the environment variables
bot.run(token)