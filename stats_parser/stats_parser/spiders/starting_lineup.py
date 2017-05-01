import scrapy
from stats_parser.spiders.xpaths import x_teams_name, x_starting_players, x_game_tables, x_bench_players

class StartingLineupSpider(scrapy.Spider):
    name = "starting_lineup"

    def start_requests(self):
        urls = [
            "http://plk.pl/mecz/45043/polski-cukier-torun---anwil-wloclawek.html",
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def remove_whitespaces(self, string):
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

        teamA_starting = game_tables[0].xpath(x_starting_players).extract()
        teamB_starting = game_tables[1].xpath(x_starting_players).extract()
        teamA_starting = self.remove_whitespaces(teamA_starting)
        teamB_starting = self.remove_whitespaces(teamB_starting)
        if len(teamA_starting) != 5 or len(teamB_starting) != 5:
            raise ValueError("One of starting fives has a incorrect number of players")

        teamA_bench = game_tables[0].xpath(x_bench_players).extract()
        teamB_bench = game_tables[1].xpath(x_bench_players).extract()
        teamA_bench = self.remove_whitespaces(teamA_bench)
        teamB_bench = self.remove_whitespaces(teamB_bench)

        return {teams[0]:{
                    "starting":teamA_starting,
                    "bench":teamA_bench,
                    },
                teams[1]:{
                    "starting":teamB_starting,
                    "bench":teamB_bench,
                },
            }
