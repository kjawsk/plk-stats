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

    def parse(self, response):
        teams = response.xpath(x_teams_name).extract()
        teams = list(map(str.strip, teams))
        if len(teams) != 2:
            raise ValueError("Number of temas is incorrect")

        starting_fives = response.xpath(x_starting_players).extract()
        starting_fives = list(map(str.strip, starting_fives))
        if len(starting_fives) != 10:
            raise ValueError("Number of players in starting fives is incorrect")
        teamA_starting = starting_fives[:5]
        teamB_starting = starting_fives[5:10]

        game_tables = response.xpath(x_game_tables)
        if len(game_tables) != 2:
            raise ValueError("Number of game tables is incorrect")
        teamA_bench = game_tables[0].xpath(x_bench_players).extract()
        teamB_bench = game_tables[1].xpath(x_bench_players).extract()
        teamA_bench = list(map(str.strip, teamA_bench))
        teamB_bench = list(map(str.strip, teamB_bench))

        return {teams[0]:{
                    "starting":teamA_starting,
                    "bench":teamA_bench,
                    },
                teams[1]:{
                    "starting":teamB_starting,
                    "bench":teamB_bench,
                },
            }
