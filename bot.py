import os
import json
import functions
from discord.ext import commands, tasks
from dotenv import load_dotenv

last_espi_timestamp = 0
last_ebi_timestamp = 0

### BOT Part ###
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')
ESPI_CHANNEL_NAME = 'espi'
ESPI_NAME_TO_CHANNEL = {}
CHANNELS_WITH_ID = {}
USERS_WITH_ID = {}

bot = commands.Bot(command_prefix="e!")


@tasks.loop(seconds=10)
async def call_on_me_espi():
    global last_espi_timestamp
    espi = functions.get_last_espi()
    if functions.is_espi_new(espi.published, last_espi_timestamp):
        last_espi_timestamp = espi.published
        await functions.send_info_to_channels(espi, bot, ESPI_NAME_TO_CHANNEL, CHANNELS_WITH_ID)


@tasks.loop(seconds=11)
async def call_on_me_ebi():
    global last_ebi_timestamp
    ebi = functions.get_last_ebi()
    if functions.is_ebi_new(ebi.published, last_ebi_timestamp):
        last_ebi_timestamp = ebi.published
        await functions.send_info_to_channels(ebi, bot, ESPI_NAME_TO_CHANNEL, CHANNELS_WITH_ID)


@call_on_me_espi.before_loop
@call_on_me_ebi.before_loop
async def before():
    await bot.wait_until_ready()
    print("Bot is ready!")


# COMMANDS
@bot.command()
# @commands.has_any_role("", "")
@commands.has_permissions(administrator=True)
async def refresh_channels(ctx, channels_with_id):
    print("Before")
    print(channels_with_id)
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
    espi = functions.get_last_espi()
    await functions.send_info_to_channels(espi, bot, ESPI_NAME_TO_CHANNEL, CHANNELS_WITH_ID)


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
    print(f"{servers}")


@bot.event
async def on_ready():
    print("I'm in!")
    for channel in bot.get_guild(int(GUILD)).channels:
        CHANNELS_WITH_ID[channel.name] = channel.id


if __name__ == "__main__":
    call_on_me_espi.start()
    call_on_me_ebi.start()
    bot.run(TOKEN)
