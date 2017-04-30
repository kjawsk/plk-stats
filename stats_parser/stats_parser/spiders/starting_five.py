import scrapy

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
        teamB_players = []
        teamA_players = []
        for idx, row in enumerate(response.xpath("//tr[td//i[@class='ico-star']]")):
            if idx < 5:
                teamA_players.append(row.xpath(".//a//strong/text()").extract_first())
            elif 4 < idx < 10:
                teamB_players.append(row.xpath(".//a//strong/text()").extract_first())
            else:
                raise ValueError("There is more than 10 players in starting fives")
        return {"teamA" : teamA_players,
                "teamB" : teamB_players}
