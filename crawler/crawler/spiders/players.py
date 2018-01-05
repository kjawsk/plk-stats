"""This is a module spider for scraping players from teams sites"""

import scrapy
from datetime import datetime
from w3lib.html import remove_tags

from stats.models import Team, Player

class PlayersSpider(scrapy.Spider):

    name = "players"
    xpath_team_name = "//*[@id='team-header']//h1/text()"
    xpath_player = "//tr[@itemprop='athlete']"

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

    def team(self, response):
        """Handles fetching team object for specified response from plk.pl"""
        team_name = response.xpath(self.xpath_team_name).extract()[0]
        try:
            team = Team.objects.get(name=team_name)
        except Team.DoesNotExist:
            team = Team.objects.create(name=team_name)
        return team

    def players(self, response):
        """Handles fetching players names for team from plk.pl"""
        extracted = response.xpath(self.xpath_player).extract()
        cleaned = [remove_tags(x.replace("  ", "")) for x in extracted]
        players = [x.split("\n") for x in cleaned]
        return players

    def parse(self, response):
        """Creates player objects for team from response"""
        team = self.team(response)
        players = self.players(response)

        for row in players:
            Player.objects.create(
                name = row[2],
                short_name = row[2].split()[0][0] + ". " + row[2].split()[1],
                team = team,
                passport = row[3],
                birth = datetime.strptime(row[4], "%Y-%m-%d"),
                height = row[5],
                position = row[6]
            )
