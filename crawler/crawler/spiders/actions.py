"""This is a module spider for scraping actions from matches
"""

import re
import scrapy
import datetime

from w3lib.html import remove_tags
from crawler.spiders.xpaths import x_home_team_name, x_away_team_name, x_date, x_play_by_play
from crawler.items import ActionItem, MatchItem
from stats.models import Action_Type, Player, Team

class ActionsSpider(scrapy.Spider):
    """Class for spiders. Responsible for extracting actions from matches specifed in url defined in
    start_requests"""

    name = "actions"
    actions_mapper = {
        "C2PKT" : [" celny ", "2 pkt"],
        "N2PKT" : [" niecelny ", "2 pkt"],
        "Z2PKT" : [" zablokowany ", "2 pkt"],
        "C3PKT" : [" celny ", "3 pkt"],
        "N3PKT" : [" niecelny ", "3 pkt"],
        "Z3PKT" : [" zablokowany ", "3 pkt"],
    }
    response = None

    def start_requests(self):
        """Provides list of matches to scrap"""
        urls = [
            "http://plk.pl/mecz/45043/polski-cukier-torun---anwil-wloclawek.html",
            # "http://plk.pl/mecz/44792/miasto-szkla-krosno---rosa-radom.html"
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    @staticmethod
    def remove_extra_whitespaces(string):
        """Scraped actions contains unexpected, extra spaces in player, team names and in actions.
        This method rewrites string with only one space.
        """
        result = list(map(str.split, string))
        result = [' '.join(x) for x in result]
        return result

    def actions(self):
        """Method to scrap actions from response. Return a list of all action from match in form:
            ["9:45 N. Player shoot for 2 pkt"] for home team actions or
            ["N. Player shoot for 2 pkt 9:45"] for away team actions
        Logic flow:
        1. get actions from specified quart
        2. remove tags from actions and ommit no-brake space sign
        3. link each action with time of this action to one list item
        4. remove extra whitespaces from actions and cut it as needed
        """
        result = []
        for quart in range(1, 5):
            xpath = x_play_by_play[quart]
            extracted = self.response.xpath(xpath).extract()
            cleaned = [remove_tags(x) for x in extracted if x != "<td>\xa0</td>"]
            linked = [cleaned[i]+cleaned[i-1] for i in range(len(cleaned)) if i % 2 == 0]
            #for 1st quart first two plays are always empty => "10:00"
            #for 2nd-4th quart first play are always empty => "10:00"
            offset = 2 if quart == 1 else 1
            #for 4th quart last action is empty
            if quart == 4:
                result += self.remove_extra_whitespaces(linked)[offset:-1]
            else:
                result += self.remove_extra_whitespaces(linked)[offset:]
        return result

    def date(self):
        """Used to get date of match. It is extracted from response"""
        date = self.response.xpath(x_date).extract()
        date = re.search(r'(\d{2}.\d{2}.\d{4})', date[2]).group(1)
        date = datetime.datetime.strptime(date, "%d.%m.%Y").strftime("%Y-%m-%d")
        return date

    def add_match(self):
        """Used to add match and return it, based on extracted team names and date, if team does
        not exist in db error is logged and exception is reraised"""
        home_team_name = "".join(self.response.xpath(x_home_team_name).extract())
        away_team_name = "".join(self.response.xpath(x_away_team_name).extract())
        try:
            home_team = Team.objects.get(name=home_team_name)
            away_team = Team.objects.get(name=away_team_name)
        except Team.DoesNotExist:
            self.logger.critical(
                "%s, %s: one of these team names not found in db during parsing: %s" %
                (home_team_name, away_team_name, self.response.url)
            )
            raise
        else:
            match = MatchItem()
            match['home_team'] = home_team
            match['away_team'] = away_team
            match['date'] = self.date()
            match = match.save()
            return match

    def player(self, action):
        """Used to get player object from db based on name, if player does not exist in db
        error is logged and exception is reraised"""
        try:
            player_name = re.search(r"\w+\.+\s+[\w]+", action).group()
            result = Player.objects.get(name=player_name)
        except Player.DoesNotExist:
            self.logger.critical(
                "%s: Player not found in db during parsing: %s" %
                (player_name, self.response.url)
            )
            raise
        else:
            return result

    def action_type(self, name):
        """Used to get action type object from db based on name, if name does not exist in db
        error is logged and exception is reraised"""
        try:
            result = Action_Type.objects.get(name=name)
        except Action_Type.DoesNotExist:
            self.logger.critical(
                "%s: Action type not found in db during parsing: %s" %
                (name, self.response.url)
            )
            raise
        else:
            return result

    def parse(self, response):
        """Used to parse response. For each extracted action, which has been found in
        actions_mapper, action object is created and stored in db"""
        self.response = response
        match = self.add_match()
        for action in self.actions():
            for action_type, key_words in self.actions_mapper.items():
                if all(word in action for word in key_words):
                    item = ActionItem()
                    item["match"] = match
                    item["action_type"] = self.action_type(action_type)
                    item["player"] = self.player(action)
                    item["time"] = re.search(r"\d{2}:\d{2}", action).group()
                    item.save()
