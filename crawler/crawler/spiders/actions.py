"""This is a module spider for scraping actions from matches
"""

import scrapy
import json
import datetime;

from crawler.items import ActionItem, MatchItem
from stats.models import Action, Action_Type, Player, Team

class ActionsSpider(scrapy.Spider):

    name = "actions"

    def start_requests(self):
        """Provides list of matches to scrap"""
        urls = [
            "http://www.fibalivestats.com/data/742430/data.json",
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def add_match(self):
        """"""
        try:
            home_team_name = self.data['tm']['1']['name']
            away_team_name = self.data['tm']['2']['name']
            self.home_team = Team.objects.get(name=home_team_name)
            self.away_team = Team.objects.get(name=away_team_name)
        except Team.DoesNotExist:
            self.logger.critical(
                "%s, %s: one of these team names not found in db during parsing: %s" %
                (home_team_name, away_team_name, self.response.url)
            )
            raise
        except KeyError:
            self.logger.critical(
                "Name field not found in json from %s" % (self.response.url)
            )
        else:
            match = MatchItem()
            match['home_team'] = self.home_team
            match['away_team'] = self.away_team
            match['date'] = datetime.datetime.now()
            match = match.save()
            return match

    def parse(self, response):
        self.data = json.loads(response.body_as_unicode())
        match = self.add_match()

        for play in self.data['pbp']:
            if play['actionType'] == '2pt':
                player_name = play['firstName'] + " " + play['familyName']
                item = ActionItem()
                item["match"] = match
                item["team"] = self.home_team if play['tno'] == 1 else self.away_team
                item["action_type"] = Action_Type.objects.get(name=play['actionType'])
                item["player"] = Player.objects.get(name=player_name)
                item["time"] = play['gt']
                item.save()
