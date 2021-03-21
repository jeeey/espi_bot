from espi_provider import EspiProvider
from discord.ext import commands, tasks


class EspiTaskCog(commands.Cog):

    def __init__(self, bot, espi_sender):
        self.bot = bot
        self.espi_sender = espi_sender
        self.espi_provider = EspiProvider()

        self.last_espi_timestamp = 0
        self.last_ebi_timestamp = 0

        self.call_on_me_espi.start()
        self.call_on_me_ebi.start()

    def __is_espi_new(self, espi_timestamp):
        return self.last_espi_timestamp != espi_timestamp

    def __is_ebi_new(self, ebi_timestamp):
        return self.last_ebi_timestamp != ebi_timestamp

    @tasks.loop(seconds=5)
    async def call_on_me_espi(self):
        espi = self.espi_provider.get_last_espi()
        if self.__is_espi_new(espi.published):
            self.last_espi_timestamp = espi.published
            await self.espi_sender.send_info_to_channels(espi)

    @tasks.loop(seconds=6)
    async def call_on_me_ebi(self):
        ebi = self.espi_provider.get_last_ebi()
        if self.__is_ebi_new(ebi.published):
            self.last_ebi_timestamp = ebi.published
            await self.espi_sender.send_info_to_channels(ebi)

    @call_on_me_espi.before_loop
    @call_on_me_ebi.before_loop
    async def before(self):
        await self.bot.wait_until_ready()
        print("Bot is ready!")

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def resend_last_espi(self, ctx):
        espi = self.espi_provider.get_last_espi()
        await self.espi_sender.send_info_to_channels(espi)
