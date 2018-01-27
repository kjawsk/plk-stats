from datetime import datetime
from stats.models import Team, Player, Team_Player

class PlayersPipeline(object):
    """This is a class responsible for processing(adding to database) items from players spider"""

    def _current_players(self, current_players, team):
        """Creates or gets player objects, then create Team Player object, if player has already
        exist for team, this action is omitted."""
        players_in_db = Team_Player.objects.filter(team=team)
        for player in current_players:
            if not players_in_db.filter(player__name=player[2]).exists():
                player, created = Player.objects.get_or_create(
                    name = player[2],
                    short_name = player[2].split()[0][0] + ". " + player[2].split()[1],
                    passport = player[3],
                    birth = datetime.strptime(player[4], "%Y-%m-%d"),
                    height = player[5],
                    position = player[6]
                )
                Team_Player.objects.create(
                    team=team,
                    player=player,
                    to=None
                )

    def _past_players(self, past_players, team):
        """Creates or gets player objects, then create Team Player object, if player has already
        exist for team, this action is omitted."""
        players_in_db = Team_Player.objects.filter(team=team)
        for player in past_players:
            if not players_in_db.filter(player__name=player).exists():
                player, created  = Player.objects.get_or_create(
                        name=player,
                        short_name=player.split()[0][0] + ". " + player.split()[1]
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
