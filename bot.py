import os
from espi_task_cog import EspiTaskCog
from espi_sender import EspiSender
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')

bot = commands.Bot(command_prefix="e!")


@bot.command()
@commands.has_permissions(administrator=True)
async def print_servers(ctx):
    servers = list(bot.guilds)
    print(f"{servers}")


if __name__ == "__main__":
    espi_sender = EspiSender(bot, int(GUILD))
    bot.add_cog(espi_sender)
    bot.add_cog(EspiTaskCog(bot, espi_sender))
    bot.run(TOKEN)
