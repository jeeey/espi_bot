import os
from espi_tasks import EspiTasks
from espi_sender import EspiSender
from espi_provider import EspiProvider
from espi_commands import EspiCommands
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')


if __name__ == "__main__":
    bot = commands.Bot(command_prefix="e!")
    espi_provider = EspiProvider()
    espi_sender = EspiSender(bot, int(GUILD))

    bot.add_cog(EspiCommands(bot, espi_provider, espi_sender))
    bot.add_cog(EspiTasks(bot, espi_provider, espi_sender))
    bot.run(TOKEN)
