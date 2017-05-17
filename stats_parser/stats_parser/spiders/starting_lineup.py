"""This is a module spider for scraping starting fives
TODO: Refactoring with item loaders and processors; docstrings for refacored method
"""

import scrapy
from stats_parser.spiders.xpaths import (
    x_bench_players, x_game_tables, x_starting_players, x_teams_name
)

class StartingLineupSpider(scrapy.Spider):
    name = "starting_lineup"

    def start_requests(self):
        urls = [
            "http://plk.pl/mecz/45043/polski-cukier-torun---anwil-wloclawek.html",
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    @staticmethod
    def remove_whitespaces(string):
        result = list(map(str.split, string))
        result = [' '.join(x) for x in result]
        return result

    def parse(self, response):
        teams = response.xpath(x_teams_name).extract()
        teams = self.remove_whitespaces(teams)
        if len(teams) != 2:
            raise ValueError("Number of teams is incorrect")

        game_tables = response.xpath(x_game_tables)
        if len(game_tables) != 2:
            raise ValueError("Number of game tables is incorrect")

        home_team_starting = game_tables[0].xpath(x_starting_players).extract()
        away_team_starting = game_tables[1].xpath(x_starting_players).extract()
        home_team_starting = self.remove_whitespaces(home_team_starting)
        away_team_starting = self.remove_whitespaces(away_team_starting)
        if len(home_team_starting) != 5 or len(away_team_starting) != 5:
            raise ValueError("One of starting fives has a incorrect number of players")

        home_team_bench = game_tables[0].xpath(x_bench_players).extract()
        away_team_bench = game_tables[1].xpath(x_bench_players).extract()
        home_team_bench = self.remove_whitespaces(home_team_bench)
        away_team_bench = self.remove_whitespaces(away_team_bench)

        return {
            teams[0]:{
                "starting":home_team_starting,
                "bench":home_team_bench,
            },
            teams[1]:{
                "starting":away_team_starting,
                "bench":away_team_bench,
            },
        }
