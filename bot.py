import os
import feedparser
import json
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
ESPI_NAME_TO_CHANNEL = {}
CHANNELS_WITH_ID = {}
USERS_WITH_ID = {}

bot = commands.Bot(command_prefix="e!")


async def send_info_to_channel(name, info):
    channel = bot.get_channel(CHANNELS_WITH_ID[name])
    await channel.send(format_espi(info))


async def send_info_to_user(name, info):
    user = bot.get_user(USERS_WITH_ID[name])
    await user.send(format_espi(info))


async def send_info_to_channels(info):

    espi_title = info.title.split()
    stock_name = espi_title[0]
    channels = [val for key, val in ESPI_NAME_TO_CHANNEL.items() if stock_name in key]

    title_size = 2
    while len(channels) > 1:
        for i in range(1, title_size):
            stock_name = stock_name + " " + espi_title[i]
            channels = [val for key, val in ESPI_NAME_TO_CHANNEL.items() if stock_name in key]
        title_size += 1

    if len(channels) == 1:
        message_channel = bot.get_channel(CHANNELS_WITH_ID[channels[0]])
        print(f"Sending espi to {message_channel}")
        await message_channel.send(format_espi(info))
    else:
        print("No channel!")

    message_channel = bot.get_channel(CHANNELS_WITH_ID[ESPI_CHANNEL_NAME])
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


# COMMANDS
@bot.command()
# @commands.has_any_role("", "")
@commands.has_permissions(administrator=True)
async def refresh_channels(ctx):
    print("Before")
    print(CHANNELS_WITH_ID)
    for channel in bot.get_all_channels():
        CHANNELS_WITH_ID[channel.name] = channel.id
    print("After")
    print(CHANNELS_WITH_ID)


@bot.command(brief='e!sub "NAZWA SPOLKI Z ESPI" "kanal"')
@commands.has_permissions(administrator=True)
async def sub(ctx, espi_name, channel_name):
    await refresh_channels(ctx)
    ESPI_NAME_TO_CHANNEL[espi_name] = channel_name
    message_channel = bot.get_channel(CHANNELS_WITH_ID[channel_name])
    await message_channel.send(f"Rejestracja {espi_name}")


@bot.command(brief='e!unsub "NAZWA SPOLKI Z ESPI"')
@commands.has_permissions(administrator=True)
async def unsub(ctx, espi_name):
    message_channel = bot.get_channel(CHANNELS_WITH_ID[ESPI_NAME_TO_CHANNEL[espi_name]])
    await message_channel.send(f"Derejestracja {espi_name}")
    ESPI_NAME_TO_CHANNEL.pop(espi_name)


@bot.command()
@commands.has_permissions(administrator=True)
async def resend_last_espi(ctx):
    espi = get_last_espi()
    await send_info_to_channels(espi)


@bot.command(brief='Wypisanie wszystkich subskrybcji')
@commands.has_permissions(administrator=True)
async def get_subs(ctx):
    await ctx.channel.send(ESPI_NAME_TO_CHANNEL)

@bot.command(brief='Zaladuj backup przypisan')
@commands.has_permissions(administrator=True)
async def load_subs(ctx):
    global ESPI_NAME_TO_CHANNEL
    with open('subs_backup.txt') as file:
       data = file.read()

    ESPI_NAME_TO_CHANNEL = json.loads(data)
    print(ESPI_NAME_TO_CHANNEL)

@bot.command()
@commands.has_permissions(administrator=True)
async def print_servers(ctx):
    servers = list(bot.guilds)
    for s in servers:
        print(f"{s}")


@bot.event
async def on_ready():
    print("I'm in!")
    for channel in bot.get_guild(int(GUILD)).channels:
        CHANNELS_WITH_ID[channel.name] = channel.id


#MAIN
call_on_me_espi.start()
call_on_me_ebi.start()
bot.run(TOKEN)
