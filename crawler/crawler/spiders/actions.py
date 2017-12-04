"""This is a module spider for scraping actions from matches
"""

import datetime;
import json
import scrapy
import re

from crawler.items import ActionItem, MatchItem
from stats.models import Action, Action_Type, Action_Subtype, Player, Team, Match

class ActionsSpider(scrapy.Spider):

    name = "actions"

    def start_requests(self):
        """Provides list of matches to scrap"""
        urls = [
            "http://www.fibalivestats.com/data/742430/data.json",
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def match_from_response(self, response):
        fiba_id = re.search(r'\d+', response.url).group()
        if fiba_id is not None:
            try:
                match = Match.objects.get(fiba_id=fiba_id)
            except Match.DoesNotExist:
                self.logger.critical(
                    "\n------\Match with following fiba_id does not exist in db: %s\n"%
                    (fiba_id)
                )
            else:
                return match
        self.logger.critical(
            "\n------\Fiba id not found in following url: %s\n"%
            (response.url)
        )

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
        finally:
            return {
                'type' : action_type,
                'subtype' : action_subtype,
            }

    def parse(self, response):
        self.data = json.loads(response.body_as_unicode())
        match = self.match_from_response(response)

        for play in self.data['pbp']:
            if play['actionType'] == '2pt':
                player_name = play['firstName'] + " " + play['familyName']
                play_type = self.action_type(play)
                item = ActionItem()
                item['match'] = match
                item['team'] = match.home_team if play['tno'] == 1 else match.away_team
                item['action_type'] = play_type['type']
                item['action_subtype'] = play_type['subtype']
                item['player'] = Player.objects.get(name=player_name)
                item['time'] = datetime.datetime.strptime(play['gt'], '%M:%S').time()
                ## TODO add period field
                item.save()
