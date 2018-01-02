"""This is a module spider for scraping actions from matches
"""

import datetime
import json
import scrapy
import re

from crawler.items import ActionItem
from stats.models import Action, Action_Type, Action_Subtype, Player, Match, Period_Type

class ActionsSpider(scrapy.Spider):
    """Class ActionsSpider is responsible for fetching actions from fibalivestats for matches
    defined in urls variable(in start_requests)"""

    name = "actions"

    def start_requests(self):
        """Provides list of matches to scrap"""
        urls = [
            # "http://www.fibalivestats.com/data/771009/data.json",
            "http://www.fibalivestats.com/data/742430/data.json",
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def match_from_response(self, response):
        """"Handles fetching match from db based on fiba_id"""
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
        """Handles fetching action type for specified play"""
        try:
            action_type = Action_Type.objects.get(name=play['actionType'])
        except Action_Type.DoesNotExist:
            self.logger.critical(
                "\n------\nAction type does not exist in db: %s\n"%
                (play['actionType'])
            )
            raise
        else:
            return action_type

    def player(self, play):
        """Handles fetching player for specified play"""
        player_name = play['firstName'] + " " + play['familyName']
        try:
            player = Player.objects.get(name=player_name)
        except Player.DoesNotExist:
            self.logger.critical(
                "\n------\nPlayer does not exist in db: %s\n"%
                (player_name)
            )
            raise
        else:
            return player

    def action_subtype(self, play):
        """Handles fetching action subtype for specified play"""
        try:
            action_subtype = Action_Subtype.objects.get(name=play['subType'])
        except Action_Subtype.DoesNotExist:
            self.logger.debug(
                "\n------\nAction subtype does not exist in db: %s\n"%
                (play['subType'])
            )
            action_subtype = None
        finally:
            return action_subtype

    def period_type(self, play):
        """Handles fetching period type for specified play"""
        try:
            period_type = Period_Type.objects.get(name=play['periodType'])
        except Period_Type.DoesNotExist:
            self.logger.critical(
                "\n------\nPeriod type does not exist in db: %s\n"%
                (play['periodType'])
            )
            raise
        else:
            return period_type

    def parse(self, response):
        """Builds action model object for each fetched action from fibalivestats"""
        self.data = json.loads(response.body_as_unicode())
        match = self.match_from_response(response)

        for play in self.data['pbp']:
            if play['actionType'] == '2pt':
                item = ActionItem()
                item['match'] = match
                item['team'] = match.home_team if play['tno'] == 1 else match.away_team
                item['action_type'] = self.action_type(play)
                item['action_subtype'] = self.action_subtype(play)
                item['player'] = self.player(play)
                item['time'] = datetime.datetime.strptime(play['gt'], '%M:%S').time()
                item['success'] = True if play['success'] == 1 else False
                item['period_type'] = self.period_type(play)
                item['period'] =  play['period']
                item.save()
