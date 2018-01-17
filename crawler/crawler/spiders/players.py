"""This is a module spider for scraping players from teams sites"""

import scrapy
from datetime import datetime
from w3lib.html import remove_tags

from stats.models import Team, Player, TeamPlayer

class PlayersSpider(scrapy.Spider):

    name = "players"
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

    def team(self, response):
        """Handles fetching team object for specified response from plk.pl"""
        team_name = response.xpath(self.xpath_team_name).extract()[0]
        team, created = Team.objects.get_or_create(name=team_name)
        return team

    def past_players(self, response, team):
        """Handles fetching past players(past coach names are omitted) names for team from plk.pl and
        creates player objects for team from response, if player has already exist for team,
        this action is omitted"""
        infos = response.xpath(self.xpath_past_crew_infos).extract()
        infos = [x.replace(",", "").strip() for x in infos]
        names = response.xpath(self.xpath_past_crew_names).extract()
        past_crew = list(zip(names, infos))
        past_players = [x for x in past_crew if 'zawodnik' in x[1]]

        players_db = TeamPlayer.objects.filter(team__name=team)
        for player in past_players:
            if not players_db.filter(team__name=player[0]).exists():
                player, created  = Player.objects.get_or_create(
                        name=player[0],
                        short_name=player[0].split()[0][0] + ". " + player[0].split()[1]
                    )
                TeamPlayer.objects.create(
                    team=team,
                    player=player,
                    to=None
                )

    def current_players(self, response, team):
        """Handles fetching players names for team from plk.pl and creates player objects for team
        from response, if player has already exist for team, this action is omitted"""
        extracted = response.xpath(self.xpath_player).extract()
        cleaned = [remove_tags(x.replace("  ", "")) for x in extracted]
        players_plk = [x.split("\n") for x in cleaned]

        players_db = TeamPlayer.objects.filter(team__name=team)
        for player in players_plk:
            if not players_db.filter(team__name=player[2]).exists():
                player, created = Player.objects.get_or_create(
                    name = player[2],
                    short_name = player[2].split()[0][0] + ". " + player[2].split()[1],
                    passport = player[3],
                    birth = datetime.strptime(player[4], "%Y-%m-%d"),
                    height = player[5],
                    position = player[6]
                )
                TeamPlayer.objects.create(
                    team=team,
                    player=player,
                    to=None
                )


    def parse(self, response):
        """Parses response from each team site from plk.pl"""
        team = self.team(response)
        self.current_players(response, team)
        self.past_players(response, team)
