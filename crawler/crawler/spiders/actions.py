"""This is a module spider for scraping each play from matches
TODO: Refactoring with item loaders and processors; docstrings for refacored method
"""

import re
import scrapy
import datetime

from w3lib.html import remove_tags
from crawler.spiders.xpaths import x_home_team_name, x_away_team_name, x_date, x_play_by_play
from crawler.items import ActionItem, MatchItem
from stats.models import Action_Type, Player, Team

class ActionsSpider(scrapy.Spider):
    name = "actions"

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

    def actions(self, response):
        result = []
        for quart in range(1, 5):
            xpath = x_play_by_play[quart]
            extracted = response.xpath(xpath).extract()
            cleaned = [remove_tags(x) for x in extracted if x != "<td>\xa0</td>"]
            linked = [cleaned[i]+cleaned[i-1] for i in range(len(cleaned)) if i % 2 == 0]
            #for 1st quart first two plays are always empty => "10:00"
            #for 2nd-4th quart first play are always empty => "10:00"
            offset = 2 if quart == 1 else 1
            #for 4th quart last action is empty
            if quart == 4:
                result += self.remove_whitespaces(linked)[offset:-1]
            else:
                result += self.remove_whitespaces(linked)[offset:]
        return result

    def date(self, response):
        date = response.xpath(x_date).extract()
        date = re.search(r'(\d{2}.\d{2}.\d{4})', date[2]).group(1)
        date = datetime.datetime.strptime(date, "%d.%m.%Y").strftime("%Y-%m-%d")
        return date

    def parse(self, response):
        home_team_name = "".join(response.xpath(x_home_team_name).extract())
        away_team_name = "".join(response.xpath(x_away_team_name).extract())
        home_team = Team.objects.get(name=home_team_name)
        away_team = Team.objects.get(name=away_team_name)

        match = MatchItem()
        match['home_team'] = home_team
        match['away_team'] = away_team
        match['date'] = self.date(response)
        match = match.save()

        for action in self.actions(response):
            if "celny" in action and "2 pkt" in action and "niecelny" not in action:
                action_type = Action_Type.objects.get(name="C2PKT")
                player_name = re.search(r"\w+\.+\s+[\w]+", action).group()
                player = Player.objects.get(name=player_name)
                time = re.search(r"\d{2}:\d{2}", action).group()

                action = ActionItem()
                action["match"] = match
                action["action_type"] = action_type
                action["player"] = player
                action["time"] = time
                action.save()
