"""This is a module spider for scraping each play from matches
TODO: Refactoring with item loaders and processors; docstrings for refacored method
"""

import re
import scrapy

from w3lib.html import remove_tags
from crawler.spiders.xpaths import x_play_by_play

class PlayByPlaySpider(scrapy.Spider):
    name = "play_by_play"

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

    def get_actions_from_quart(self, response, quart):
        xpath = x_play_by_play[quart]
        extracted = response.xpath(xpath).extract()
        cleaned = [remove_tags(x) for x in extracted if x != "<td>\xa0</td>"]
        linked = [cleaned[i]+cleaned[i-1] for i in range(len(cleaned)) if i % 2 == 0]
        #for 1st quart first two plays are always empty => "10:00"
        #for 2nd-4th quart first play are always empty => "10:00"
        offset = 2 if quart == 1 else 1
        #for 4th quart last action is empty
        if quart == 4:
            return self.remove_whitespaces(linked)[offset:-1]
        else:
            return self.remove_whitespaces(linked)[offset:]

    def parse(self, response):
        actions = self.get_actions_from_quart(response, 1)
        actions += self.get_actions_from_quart(response, 2)
        actions += self.get_actions_from_quart(response, 3)
        actions += self.get_actions_from_quart(response, 4)
        regex = re.compile(r"\d{2}:\d{2}")
        for action in actions:
            time = regex.search(action).group()
            yield {
                "team": "home" if regex.match(action) else "away",
                "time": time,
                "action": action.replace(time, "").strip(),
            }
