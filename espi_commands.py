from discord.ext import commands


class EspiCommands(commands.Cog):

    def __init__(self, bot, espi_provider, espi_sender):
        self.bot = bot
        self.espi_provider = espi_provider
        self.espi_sender = espi_sender

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def resend_last_espi(self, ctx):
        espi = self.espi_provider.get_last_espi()
        await self.espi_sender.send_info_to_channels(espi)

    @commands.command()
    # @commands.has_any_role("", "")
    @commands.has_permissions(administrator=True)
    async def refresh_channels(self, ctx):
        await self.espi_sender.refresh_channels_list()

    @commands.command(brief='e!sub "NAZWA SPOLKI Z ESPI" "kanal"')
    @commands.has_permissions(administrator=True)
    async def sub(self, ctx, espi_name, channel_name):
        await self.espi_sender.subscribe(espi_name, channel_name)

    @commands.command(brief='e!unsub "NAZWA SPOLKI Z ESPI"')
    @commands.has_permissions(administrator=True)
    async def unsub(self, ctx, espi_name):
        await self.espi_sender.unsubscribe(espi_name)

    @commands.command(brief='Wypisanie wszystkich subskrybcji')
    @commands.has_permissions(administrator=True)
    async def get_subs(self, ctx):
        await self.espi_sender.get_subs(ctx)

    @commands.command(brief='Zaladuj backup przypisan')
    @commands.has_permissions(administrator=True)
    async def load_subs(self, ctx):
        await self.espi_sender.load_subs()

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def print_servers(self, ctx):
        await ctx.channel.send(list(self.bot.guilds))
