import feedparser


class EspiProvider:

    def __init__(self):
        self.espi_rss_url = "http://biznes.pap.pl/pl/rss/6614"
        self.ebi_rss_url = "http://biznes.pap.pl/pl/rss/6612"

    def get_last_espi(self):
        return feedparser.parse(self.espi_rss_url).entries[0]

    def get_last_ebi(self):
        return feedparser.parse(self.ebi_rss_url).entries[0]
