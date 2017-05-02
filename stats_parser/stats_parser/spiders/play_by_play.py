import scrapy
import re

from w3lib.html import remove_tags
from stats_parser.spiders.xpaths import x_play_by_play

class PlayByPlaySpider(scrapy.Spider):
    name = "play_by_play"

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
        extracted = response.xpath(x_play_by_play).extract()
        without_tags = [remove_tags(x) for x in extracted if x != '<td>\xa0</td>']
        without_tags = [without_tags[i]+" "+without_tags[i-1] for i in range(len(without_tags)) if i % 2 == 0]
        actions = self.remove_whitespaces(without_tags)[2:]
        regex = re.compile("\d{2}:\d{2}")
        for action in actions:
            time = regex.search(action).group()
            yield {
                "team": "home" if regex.match(action) else "away",
                "time": time,
                "action": action.replace(regex.search(time).group(), "").strip(),
            }
