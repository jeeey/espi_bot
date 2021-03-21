import json
from discord.ext import commands


class EspiSender(commands.Cog):

    def __init__(self, bot, guild_id):
        self.bot = bot
        self.guild_id = guild_id
        self.default_espi_channel = 'espi'

        self.espi_name_to_channel = {}
        self.channels_with_id = {}

    def __format_espi(self, info):
        formated_espi = info.title + "\n" + info.published + "\n" + info.link
        return formated_espi

    async def send_info_to_channel(self, info, channel_name):
        channel = self.bot.get_channel(self.channels_with_id[channel_name])
        print(f"Sending espi to {channel}")
        await channel.send(self.__format_espi(info))

    async def send_info_to_channels(self, info):
        espi_title = info.title.split()
        stock_name = espi_title[0]
        channels = [val for key, val in self.espi_name_to_channel.items() if stock_name in key]

        title_size = 2
        while len(channels) > 1:
            for i in range(1, title_size):
                stock_name = stock_name + " " + espi_title[i]
                channels = [val for key, val in self.espi_name_to_channel.items() if stock_name in key]
            title_size += 1

        if len(channels) == 1:
            await self.send_info_to_channel(info, channels[0])
        else:
            print("No channel!")

        await self.send_info_to_channel(info, self.default_espi_channel)

    @commands.Cog.listener()
    async def on_ready(self):
        print("I'm in!")
        for channel in self.bot.get_guild(self.guild_id).channels:
            self.channels_with_id[channel.name] = channel.id

    @commands.command()
    # @commands.has_any_role("", "")
    @commands.has_permissions(administrator=True)
    async def refresh_channels(self, ctx):
        print("Before")
        print(self.channels_with_id)
        for channel in self.bot.get_all_channels():
            self.channels_with_id[channel.name] = channel.id
        print("After")
        print(self.channels_with_id)

    @commands.command(brief='e!sub "NAZWA SPOLKI Z ESPI" "kanal"')
    @commands.has_permissions(administrator=True)
    async def sub(self, ctx, espi_name, channel_name):
        await self.refresh_channels(ctx)
        self.espi_name_to_channel[espi_name] = channel_name
        message_channel = self.bot.get_channel(self.channels_with_id[channel_name])
        await message_channel.send(f"Rejestracja {espi_name}")

    @commands.command(brief='e!unsub "NAZWA SPOLKI Z ESPI"')
    @commands.has_permissions(administrator=True)
    async def unsub(self, ctx, espi_name):
        message_channel = self.bot.get_channel(self.channels_with_id[self.espi_name_to_channel[espi_name]])
        await message_channel.send(f"Derejestracja {espi_name}")
        self.espi_name_to_channel.pop(espi_name)

    @commands.command(brief='Wypisanie wszystkich subskrybcji')
    @commands.has_permissions(administrator=True)
    async def get_subs(self, ctx):
        await ctx.channel.send(self.espi_name_to_channel)

    @commands.command(brief='Zaladuj backup przypisan')
    @commands.has_permissions(administrator=True)
    async def load_subs(self, ctx):
        with open('subs_backup.txt') as file:
            data = file.read()

        self.espi_name_to_channel = json.loads(data)
        print(self.espi_name_to_channel)
