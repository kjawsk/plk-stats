import logging

from stats.models import (Action, Action_Type, Action_Subtype, Team, Team_Player, Match,
                          Period_Type, Player)


class PlayersPipeline(object):
    """This is a class responsible for processing(adding to database) items from players spider"""

    @staticmethod
    def _current_players(current_players, team):
        """Creates or gets player objects, then create Team Player object, if player has already
        exist for team, this action is omitted."""
        players_in_db = Team_Player.objects.filter(team=team)
        for player in current_players:
            if not players_in_db.filter(player__name=player['name']).exists():
                player, _ = Player.objects.get_or_create(
                    name=player['name'],
                    short_name=player['short_name'],
                    passport=player['passport'],
                    birth=player['birth'],
                    height=player['height'],
                    position=player['position']
                )
                Team_Player.objects.create(
                    team=team,
                    player=player,
                    to=None
                )

    @staticmethod
    def _past_players(past_players, team):
        """Creates or gets player objects, then create Team Player object, if player has already
        exist for team, this action is omitted."""
        players_in_db = Team_Player.objects.filter(team=team)
        for player in past_players:
            if not players_in_db.filter(player__name=player['name']).exists():
                player, _ = Player.objects.get_or_create(
                    name=player['name'],
                    short_name=player['short_name']
                )
                Team_Player.objects.create(
                    team=team,
                    player=player,
                    to=None
                )

    def process_item(self, item, spider):
        """Processes items from players spider"""
        team, _ = Team.objects.get_or_create(name=item['team_name'])
        self._current_players(item['current_players'], team)
        self._past_players(item['past_players'], team)
        return item


class ActionsPipeline(object):
    """This is a class responsible for processing(adding to database) items from actions spider"""

    def __init__(self):
        self.logger = logging.getLogger('Actions Pipeline Logger')
        self.logger.setLevel(logging.CRITICAL)
        super().__init__()

    def _match(self, fiba_id):
        """"Handles fetching match from db based on fiba_id, if specified match is not found
        exception is raised"""
        try:
            match = Match.objects.get(fiba_id=fiba_id)
        except Match.DoesNotExist:
            self.logger.critical(
                "\n------\nMatch with following fiba_id does not exist in db: %s\n" % (fiba_id)
            )
            raise
        else:
            return match

    def _player(self, player_name, team):
        """Handles fetching player for specified play, if player is not found
        exception is raised"""
        try:
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
        else:
            return player

    def _team(self, team_name):
        """Handles fetching team for specified play, if team is not found exception is raised"""
        try:
            team = Team.objects.get(name=team_name)
        except Team.DoesNotExist:
            self.logger.critical(
                "\n------\nTeam does not exist: %s\n" % (team_name)
            )
            raise
        else:
            return team

    def process_item(self, item, spider):
        """Processes items from actions spider"""

        match = self._match(item['fiba_id'])
        team = self._team(item['team'])
        action_type, _ = Action_Type.objects.get_or_create(name=item['action_type'])
        action_subtype, _ = Action_Subtype.objects.get_or_create(name=item['action_subtype'])
        player = self._player(item['player_name'],team) if item['player_name'] is not None else None
        period_type, _ = Period_Type.objects.get_or_create(name=item['period_type'])

        Action.objects.create(
            match=match,
            action_type=action_type,
            action_subtype=action_subtype,
            teamplayer=player,
            time=item['time'],
            success=item['success'],
            period_type=period_type,
            period=item['period'],
        )

        return item
