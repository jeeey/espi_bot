import feedparser

### RSS Part ###
espi_rss_url = "http://biznes.pap.pl/pl/rss/6614"
ebi_rss_url = "http://biznes.pap.pl/pl/rss/6612"



def get_last_espi():
    return feedparser.parse(espi_rss_url).entries[0]


def get_last_ebi():
    return feedparser.parse(ebi_rss_url).entries[0]


def is_espi_new(espi_timestamp, last_espi_timestamp):
    return last_espi_timestamp != espi_timestamp


def is_ebi_new(ebi_timestamp, last_ebi_timestamp):
    return last_ebi_timestamp != ebi_timestamp


def format_espi(espi):
    formated_espi = espi.title + "\n" + espi.published + "\n" + espi.link
    return formated_espi


async def send_info_to_channel(name, info, bot, channels_with_id):
    channel = bot.get_channel(channels_with_id[name])
    print(f"Sending espi to {channel}")
    await channel.send(format_espi(info))


async def send_info_to_user(name, info, bot, users_with_id):
    user = bot.get_user(users_with_id[name])
    await user.send(format_espi(info))


async def send_info_to_channels(info, bot, espi_name_to_channel, channels_with_id, default_espi_channel='espi'):

    espi_title = info.title.split()
    stock_name = espi_title[0]
    channels = [val for key, val in espi_name_to_channel.items() if stock_name in key]

    title_size = 2
    while len(channels) > 1:
        for i in range(1, title_size):
            stock_name = stock_name + " " + espi_title[i]
            channels = [val for key, val in espi_name_to_channel.items() if stock_name in key]
        title_size += 1

    if len(channels) == 1:
        await send_info_to_channel(channels[0], info, bot, channels_with_id)
    else:
        print("No channel!")

    await send_info_to_channel(default_espi_channel, info, bot, channels_with_id)

