import os
import feedparser
from discord.ext import commands, tasks
from dotenv import load_dotenv


### RSS Part ###

espi_rss_url = "http://biznes.pap.pl/pl/rss/6614"
last_espi_timestamp = 0


def get_last_espi():
    return feedparser.parse(espi_rss_url).entries[0]


def is_espi_new(espi_timestamp):
    return last_espi_timestamp != espi_timestamp


def format_espi(espi):
    formated_espi = espi.title + "\n" + espi.published + "\n" + espi.link
    return formated_espi


### BOT Part ###
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')
ESPI_CHANNEL_NAME = 'espi'

CHANNELS_WITH_ID = {}
bot = commands.Bot(command_prefix="!")


@tasks.loop(seconds=10)
async def call_on_me():
    global last_espi_timestamp
    espi = get_last_espi()
    if is_espi_new(espi.published):
        last_espi_timestamp = espi.published
        message_channel = bot.get_channel(CHANNELS_WITH_ID[ESPI_CHANNEL_NAME])
        print(f"Sending espi to {message_channel}")
        await message_channel.send(format_espi(espi))


@call_on_me.before_loop
async def before():
    await bot.wait_until_ready()
    print("Bot is ready!")

@bot.event
async def on_ready():
    print("I'm in!")
    for channel in bot.get_all_channels():
        CHANNELS_WITH_ID[channel.name] = channel.id

call_on_me.start()
bot.run(TOKEN)
