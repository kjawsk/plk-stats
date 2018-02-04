"""Tests for pipelines"""

import django
import os
import pytest
import sys
sys.path.append("/home/karol/Projects/plkStats/page/")
os.environ["DJANGO_SETTINGS_MODULE"] = "page.settings"
django.setup()
pytestmark = pytest.mark.django_db

from crawler.items import PlayerItem, TeamPlayersItem
from stats.models import Team, Player, Team_Player
from crawler.pipelines import PlayersPipeline

## https://docs.pytest.org/en/latest/example/parametrize.html#different-options-for-test-ids
PLAYERS = [
    ("John Doe", "J. Doe", "USA", "1990-05-27", "198", "shooting guard"),
    ("Kobe Bry", "K. Bry", "USA", "1991-06-27", "188", "point guard"),
    ("Big Mike", "B. Mike", "USA", "1992-07-27", "178", "small forward"),
    ("Ty Law", "T. Law", "USA", "1993-08-27", "218", "center"),
]


def players():
    for idx, _ in enumerate(PLAYERS):
        yield PLAYERS[idx]


def player_items():
    for player in players():
        name, short_name, passport, birth, height, position = player
        yield PlayerItem(
            name=name,
            short_name=short_name,
            passport=passport,
            birth=birth,
            height=height,
            position=position
        )


@pytest.fixture
def team_players():
    def wrapped(team_name):
        items = player_items()
        player_1 = items.__next__()
        player_2 = items.__next__()
        player_3 = items.__next__()
        player_4 = items.__next__()
        return TeamPlayersItem(
            team_name=team_name,
            current_players=[player_1, player_2],
            past_players=[player_3, player_4],
        )
    return wrapped


@pytest.mark.parametrize('team', ['New Team'])
def test_team_is_created(team_players, team):
    PlayersPipeline().process_item(team_players(team), "")

    assert Team.objects.filter(name=team).exists()


@pytest.mark.parametrize('team', ['New Team'])
def test_team_is_not_created_when_it_already_exists(team_players, team):
    PlayersPipeline().process_item(team_players(team), "")
    PlayersPipeline().process_item(team_players(team), "")

    assert Team.objects.filter(name=team).count() == 1


@pytest.mark.parametrize('team', ['New Team'])
def test_players_are_created(team_players, team):
    PlayersPipeline().process_item(team_players(team), "")

    for player in players():
        assert Player.objects.filter(name=player[0]).exists()


@pytest.mark.parametrize('team', ['New Team'])
def test_team_players_are_created(team_players, team):
    PlayersPipeline().process_item(team_players(team), "")

    for player in players():
        assert Team_Player.objects.filter(player__name=player[0], team__name=team).exists()


@pytest.mark.parametrize('team', ['New Team'])
def test_player_is_not_created_when_it_already_exists(team_players, team):
    PlayersPipeline().process_item(team_players(team), "")
    PlayersPipeline().process_item(team_players(team), "")

    for player in players():
        assert Player.objects.filter(name=player[0]).count() == 1


@pytest.mark.parametrize('team', ['New Team'])
def test_team_player_is_not_created_when_it_already_exists(team_players, team):
    PlayersPipeline().process_item(team_players(team), "")
    PlayersPipeline().process_item(team_players(team), "")

    for player in players():
        assert Team_Player.objects.filter(player__name=player[0], team__name=team).count() == 1



@pytest.mark.parametrize(
    'team_1, team_2', [
        ('Anwil Włocławek', 'Start Lublin')
    ]
)
def test_once_created_player_can_be_added_to_two_teams(team_players, team_1, team_2):
    PlayersPipeline().process_item(team_players(team_1), "")
    PlayersPipeline().process_item(team_players(team_2), "")

    for player in players():
        assert Player.objects.filter(name=player[0]).count() == 1
        assert Team_Player.objects.filter(player__name=player[0], team__name=team_1).count() == 1
        assert Team_Player.objects.filter(player__name=player[0], team__name=team_2).count() == 1
