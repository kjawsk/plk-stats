"""This is a module spider for scraping actions from matches
"""

import datetime
import json
import scrapy
import re

from django.db.models import Count
from stats.models import Match

class ActionsSpider(scrapy.Spider):
    """Class ActionsSpider is responsible for fetching actions from fibalivestats"""

    name = "actions"
    custom_settings = {
        'ITEM_PIPELINES': {
            'crawler.pipelines.ActionsPipeline': 300
        }
    }

    def start_requests(self):
        """Provides list of matches to scrap - matches without actions"""
        matches = Match.objects.annotate(Count('action')).filter(action__count=0)
        for match in matches:
            url = "http://www.fibalivestats.com/data/%s/data.json" % (match.fiba_id)
            yield scrapy.Request(url=url, callback=self.parse)
        yield scrapy.Request(url=url, callback=self.parse)

    def _player(self, play):
        """Handles fetching player for play, if KeyError is raised, then None is returned"""
        try:
            player_name = play['firstName'] + " " + play['familyName']
        except KeyError:
            player_name = None
        else:
            return player_name

    def parse(self, response):
        """Builds action dicts for all plays from fibalivestats match data

        @url http://www.fibalivestats.com/data/780639/data.json
        @returns items 486 486
        """
        fiba_id = re.search(r'\d+', response.url).group()
        data = json.loads(response.body_as_unicode())
        home_team_name = data['tm']['1']['name']
        away_team_name = data['tm']['2']['name']

        for play in data['pbp']:
            action = dict()
            action['fiba_id'] = fiba_id
            action['team'] = home_team_name if play['tno'] == 1 else away_team_name
            action['action_type'] = play['actionType']
            action['action_subtype'] = play['subType']
            action['player_name'] = self._player(play)
            action['time'] = datetime.datetime.strptime(play['gt'], '%M:%S').time()
            action['success'] = True if play['success'] == 1 else False
            action['period_type'] = play['periodType']
            action['period'] =  play['period']
            yield action
