"""This is a module spider for scraping players from teams sites"""

import scrapy
from w3lib.html import remove_tags


class PlayersSpider(scrapy.Spider):

    name = "players"
    custom_settings = {
        'ITEM_PIPELINES': {
            'crawler.pipelines.PlayersPipeline': 300
        }
    }

    xpath_team_name = "//*[@id='team-header']//h1/text()"
    xpath_player = "//tr[@itemprop='athlete']"
    xpath_past_crew_names = "//*[@id='contentInside']//div//p//strong/text()"
    xpath_past_crew_infos = "//*[@id='contentInside']//div//p/text()"

    def start_requests(self):
        """Provides list of team sites"""
        urls = [
            "http://plk.pl/druzyny/d/33/anwil-wloclawek.html",
            "http://plk.pl/druzyny/d/121/asseco-gdynia.html",
            "http://plk.pl/druzyny/d/32/azs-koszalin.html",
            "http://plk.pl/druzyny/d/1492/bm-slam-stal-ostrow-wielkopolski.html",
            "http://plk.pl/druzyny/d/764/czarni-slupsk.html",
            "http://plk.pl/druzyny/d/2310/gtk-gliwice.html",
            "http://plk.pl/druzyny/d/943/king-szczecin.html",
            "http://plk.pl/druzyny/d/11/legia-warszawa.html",
            "http://plk.pl/druzyny/d/1820/miasto-szkla-krosno.html",
            "http://plk.pl/druzyny/d/1490/mks-dabrowa-gornicza.html",
            "http://plk.pl/druzyny/d/115/pge-turow-zgorzelec.html",
            "http://plk.pl/druzyny/d/67/polpharma-starogard-gdanski.html",
            "http://plk.pl/druzyny/d/101/polski-cukier-torun.html",
            "http://plk.pl/druzyny/d/98/rosa-radom.html",
            "http://plk.pl/druzyny/d/769/stelmet-bc-zielona-gora.html",
            "http://plk.pl/druzyny/d/22/tbv-start-lublin.html",
            "http://plk.pl/druzyny/d/112/trefl-sopot.html",
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def _past_players(self, response):
        """Handles fetching past players(past coach names are omitted) names for team from plk.pl"""
        infos = response.xpath(self.xpath_past_crew_infos).extract()
        infos = [x.replace(",", "").strip() for x in infos]
        names = response.xpath(self.xpath_past_crew_names).extract()
        past_crew = list(zip(names, infos))
        past_players = [x[0] for x in past_crew if 'zawodnik' in x[1]]
        return past_players

    def _current_players(self, response):
        """Handles fetching players names for team from plk.pl"""
        extracted = response.xpath(self.xpath_player).extract()
        cleaned = [remove_tags(x.replace("  ", "")) for x in extracted]
        current_players = [x.split("\n") for x in cleaned]
        return current_players

    def parse(self, response):
        """Parses response from each team site from plk.pl

        @url http://plk.pl/druzyny/d/32/azs-koszalin.html
        @returns items 1
        @field_min_count past_players 3
        @field_min_count current_players 10
        @field_not_contain_value past_players Szczubiał
        @scrapes team_name current_players past_players
        """
        result = dict()
        result['team_name'] = response.xpath(self.xpath_team_name).extract()[0]
        result['current_players'] = self._current_players(response)
        result['past_players'] = self._past_players(response)
        yield result
