import scrapy
from stats_parser.spiders.xpaths import x_teams_name, x_starting_fives

class StartingFiveSpider(scrapy.Spider):
    name = "starting_five"

    def start_requests(self):
        urls = [
            "http://plk.pl/mecz/45043/polski-cukier-torun---anwil-wloclawek.html",
            "http://plk.pl/mecz/45038/mks-dabrowa-gornicza---energa-czarni-slupsk.html",
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        teams = response.xpath(x_teams_name).extract()
        if len(teams) != 2:
            raise ValueError("Number of temas is incorrect")

        starting_fives = response.xpath(x_starting_fives).extract()
        if len(starting_fives) != 10:
            raise ValueError("Number of players in starting fives is incorrect")

        teamA_players = starting_fives[:5]
        teamB_players = starting_fives[5:10]

        return {teams[0] : teamA_players,
                teams[1] : teamB_players}
