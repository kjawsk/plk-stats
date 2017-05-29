"""This is a module spider for scraping starting fives
TODO: Refactoring with item loaders and processors; docstrings for refacored method
"""

import scrapy
from scrapy.loader import ItemLoader
from stats_parser.items import MatchItem
from stats_parser.spiders.xpaths import (
     x_home_team_name, x_away_team_name, x_home_s5, x_home_bench, x_away_s5, x_away_bench, x_date
)

class StartingLineupSpider(scrapy.Spider):
    name = "starting_lineup"

    def start_requests(self):
        urls = [
            "http://plk.pl/mecz/45043/polski-cukier-torun---anwil-wloclawek.html",
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        loader = ItemLoader(item=MatchItem(), response=response)
        loader.add_xpath('home_team_name', x_home_team_name)
        loader.add_xpath('away_team_name', x_away_team_name)
        loader.add_xpath('home_s5', x_home_s5)
        loader.add_xpath('away_s5', x_away_s5)
        loader.add_xpath('home_bench', x_home_bench)
        loader.add_xpath('away_bench', x_away_bench)
        loader.add_xpath('date', x_date)
        return loader.load_item()
