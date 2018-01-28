"""This is a module spider for scraping actions from matches
"""

import datetime
import json
import scrapy
import re

from django.db.models import Count
from stats.models import Action, Action_Type, Action_Subtype, Team_Player, Match, Period_Type

class ActionsSpider(scrapy.Spider):
    """Class ActionsSpider is responsible for fetching actions from fibalivestats for matches
    defined in urls variable(in start_requests)"""

    name = "actions"

    def start_requests(self):
        """Provides list of matches to scrap"""
        matches = Match.objects.annotate(Count('action')).filter(action__count=0)
        for match in matches:
            url = "http://www.fibalivestats.com/data/%s/data.json" % (match.fiba_id)
            yield scrapy.Request(url=url, callback=self.parse)

    def _match_from_response(self, response):
        """"Handles fetching match from db based on fiba_id, if specified match is not found
        exception is raised"""
        fiba_id = re.search(r'\d+', response.url).group()
        if fiba_id is not None:
            try:
                match = Match.objects.get(fiba_id=fiba_id)
            except Match.DoesNotExist:
                self.logger.critical(
                    "\n------\Match with following fiba_id does not exist in db: %s\n"%
                    (fiba_id)
                )
                raise
            else:
                return match
        self.logger.critical(
            "\n------\Fiba id not found in following url: %s\n"%
            (response.url)
        )

    def _player(self, play, team):
        """Handles fetching player for specified play, if player is not found
        exception is raised"""
        try:
            player_name = play['firstName'] + " " + play['familyName']
            player = Team_Player.objects.get(player__name__iexact=player_name, team=team)
        except Team_Player.DoesNotExist:
            self.logger.critical(
                "\n------\nTeamPlayer does not exist: %s %s\n"%
                (team.name, player_name)
            )
            raise
        except Team_Player.MultipleObjectsReturned:
            self.logger.critical(
                "\n------\nThere are more than one player: %s %s\n"%
                (team.name, player_name)
            )
            raise
        except KeyError:
            player = None
        else:
            return player

    def parse(self, response):
        """Builds action model object for each fetched action from fibalivestats"""
        self.data = json.loads(response.body_as_unicode())
        match = self._match_from_response(response)

        for play in self.data['pbp']:
            team = match.home_team if play['tno'] == 1 else match.away_team
            action_type, created = Action_Type.objects.get_or_create(name=play['actionType'])
            action_subtype, created  = Action_Subtype.objects.get_or_create(name=play['subType'])
            player = self._player(play, team)
            time = datetime.datetime.strptime(play['gt'], '%M:%S').time()
            success = True if play['success'] == 1 else False
            period_type, created = Period_Type.objects.get_or_create(name=play['periodType'])
            period =  play['period']

            Action.objects.create(
                match= match,
                action_type=action_type,
                action_subtype=action_subtype,
                teamplayer=player,
                time=time,
                success=success,
                period_type=period_type,
                period=period,
            )
