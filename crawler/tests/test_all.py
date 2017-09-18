"""Tests for django-scrapy integration"""

import datetime
import sys
sys.path.append("/home/karol/Projects/plkStats/page/")
import os
os.environ["DJANGO_SETTINGS_MODULE"] = "page.settings"
import django
django.setup()

from django.test import TestCase
from crawler.items import TeamItem, MatchItem, ActionItem
from stats.models import Team, Match, Action, Player, Action_Type

class DjangoScrapyIntegrationTests(TestCase):
    """Tests for django-scrapy integration"""

    def test_scrapy_items_are_saved_in_db(self):
        """Checks if scrapy items(Team, Match and Action) are saved in databse
        """
        home_team = TeamItem(name='new team').save()
        assert Team.objects.count() == 1

        away_team = TeamItem(name='new team').save()
        assert Team.objects.count() == 2

        date = datetime.datetime.now()
        match = MatchItem(home_team=home_team, away_team=away_team, date=date).save()
        assert Match.objects.count() == 1

        action_type = Action_Type.objects.create(name="2PKTC")
        player = Player.objects.create(name="John Doe", team=home_team)
        ActionItem(
            match=match,
            action_type=action_type,
            player=player,
            time=datetime.datetime.now()
        ).save()
        assert Action.objects.count() == 1
