"""This is a module spider for scraping actions from matches
"""

import scrapy
import json
import datetime;

from crawler.items import ActionItem, MatchItem
from stats.models import Action, Action_Type, Action_Subtype, Player, Team

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

    def action_type(self, play):
        try:
            action_type = Action_Type.objects.get(name=play['actionType'])
            action_subtype = Action_Subtype.objects.get(parent=action_type, name=play['subType'])
        except Action_Subtype.DoesNotExist:
            self.logger.debug(
                "\n------\nAction subtype does not exist in db: %s\n"%
                (play['subType'])
            )
            action_subtype = None
        except Action_Type.DoesNotExist:
            self.logger.critical(
                "\n------\nAction type does not exist in db: %s\n"%
                (play['actionType'])
            )
            raise
        return {
            'type' : action_type,
            'subtype' : action_subtype,
        }

    def parse(self, response):
        self.data = json.loads(response.body_as_unicode())
        match = self.add_match()

        for play in self.data['pbp']:
            if play['actionType'] == '2pt':
                player_name = play['firstName'] + " " + play['familyName']
                play_type = self.action_type(play)
                item = ActionItem()
                item['match'] = match
                item['team'] = self.home_team if play['tno'] == 1 else self.away_team
                item['action_type'] = play_type['type']
                item['action_subtype'] = play_type['subtype']
                item['player'] = Player.objects.get(name=player_name)
                item['time'] = play['gt']
                item.save()
