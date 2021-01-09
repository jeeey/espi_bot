import os
import feedparser
from discord.ext import commands, tasks
from dotenv import load_dotenv

### RSS Part ###
espi_rss_url = "http://biznes.pap.pl/pl/rss/6614"
ebi_rss_url = "http://biznes.pap.pl/pl/rss/6612"
last_espi_timestamp = 0
last_ebi_timestamp = 0


def get_last_espi():
    return feedparser.parse(espi_rss_url).entries[0]


def get_last_ebi():
    return feedparser.parse(ebi_rss_url).entries[0]


def is_espi_new(espi_timestamp):
    return last_espi_timestamp != espi_timestamp


def is_ebi_new(ebi_timestamp):
    return last_ebi_timestamp != ebi_timestamp


def format_espi(espi):
    formated_espi = espi.title + "\n" + espi.published + "\n" + espi.link
    return formated_espi


def is_stock(stock_name, espi_title):
    return stock_name in espi_title


### BOT Part ###
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')
ESPI_CHANNEL_NAME = 'espi'

CHANNELS_WITH_ID = {}
bot = commands.Bot(command_prefix="!")


async def send_info_to_channel(name, info):
    channel = bot.get_channel(CHANNELS_WITH_ID[name])
    await channel.send(format_espi(info))


async def send_info_to_channels(info):
    message_channel = bot.get_channel(CHANNELS_WITH_ID[ESPI_CHANNEL_NAME])

    if is_stock("INNO-GENE", info.title):
        await send_info_to_channel('innogene', info)
    elif is_stock("X-TRADE BROKERS", info.title):
        await send_info_to_channel('xtb', info)
    elif is_stock("MERCATOR", info.title):
        await send_info_to_channel('mercator', info)
    elif is_stock("ALLEGRO.EU", info.title):
        await send_info_to_channel('allegro', info)
    elif is_stock("BIOMED", info.title):
        await send_info_to_channel('biomed', info)
    elif is_stock("GRODNO", info.title):
        await send_info_to_channel('grodno', info)

    print(f"Sending espi to {message_channel}")
    await message_channel.send(format_espi(info))


@tasks.loop(seconds=10)
async def call_on_me_espi():
    global last_espi_timestamp
    espi = get_last_espi()
    if is_espi_new(espi.published):
        last_espi_timestamp = espi.published
        await send_info_to_channels(espi)


@tasks.loop(seconds=11)
async def call_on_me_ebi():
    global last_ebi_timestamp
    ebi = get_last_ebi()
    if is_ebi_new(ebi.published):
        last_ebi_timestamp = ebi.published
        await send_info_to_channels(ebi)


@call_on_me_espi.before_loop
@call_on_me_ebi.before_loop
async def before():
    await bot.wait_until_ready()
    print("Bot is ready!")


@bot.event
async def on_ready():
    print("I'm in!")
    for channel in bot.get_all_channels():
        CHANNELS_WITH_ID[channel.name] = channel.id


#MAIN
call_on_me_espi.start()
call_on_me_ebi.start()
bot.run(TOKEN)
