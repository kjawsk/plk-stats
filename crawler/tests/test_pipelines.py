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


@pytest.fixture
def player_item(name):
    return PlayerItem(
        name=name,
        short_name=name.split()[0][0] + ". " + name.split()[1],
        passport="USA",
        birth="1990-08-27",
        height="198",
        position="point guard"
    )


@pytest.fixture
def team_players_item():
    player_1 = player_item("John Doe")
    player_2 = player_item("Kobe Bry")
    player_3 = player_item("Big Mike")
    player_4 = player_item("Ty Law")
    return TeamPlayersItem(
        team_name="New Team",
        current_players=[player_1, player_2],
        past_players=[player_3, player_4],
    )


def test_team_is_added(team_players_item):
    PlayersPipeline().process_item(team_players_item, "")

    assert Team.objects.filter(name="New Team").exists()


def test_team_is_not_added_when_it_already_exists(team_players_item):
    Team.objects.create(name="New Team")
    PlayersPipeline().process_item(team_players_item, "")

    assert Team.objects.filter(name="New Team").count() == 1


def test_players_are_added(team_players_item):
    PlayersPipeline().process_item(team_players_item, "")

    assert Player.objects.filter(name="John Doe").exists()
    assert Player.objects.filter(name="Kobe Bry").exists()
    assert Player.objects.filter(name="Big Mike").exists()
    assert Player.objects.filter(name="Ty Law").exists()


def test_team_players_are_added(team_players_item):
    PlayersPipeline().process_item(team_players_item, "")

    assert Team_Player.objects.filter(player__name="John Doe", team__name="New Team").exists()
    assert Team_Player.objects.filter(player__name="Kobe Bry", team__name="New Team").exists()
    assert Team_Player.objects.filter(player__name="Big Mike", team__name="New Team").exists()
    assert Team_Player.objects.filter(player__name="Ty Law", team__name="New Team").exists()


def test_player_is_not_added_when_it_already_exists(team_players_item):
    Player.objects.create(
        name="John Doe",
        short_name="J. Doe",
        passport="USA",
        birth="1990-08-27",
        height="198",
        position="point guard",
    )
    PlayersPipeline().process_item(team_players_item, "")

    assert Player.objects.filter(name="John Doe").count() == 1

