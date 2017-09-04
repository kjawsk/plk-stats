"""
Test are created mainly for refactoring purposes, they use fake_response_from_file function from
responses module.
"""

import ast

import sys
sys.path.append("/home/karol/Projects/plkStats/page/")
import os
os.environ["DJANGO_SETTINGS_MODULE"] = "page.settings"
import django
django.setup()

from crawler.items import TeamItem
from stats.models import Team

def test_item_is_saved_in_db():
    """Test for scrapy - django orm integration"""
    before = Team.objects.count()
    team_item = TeamItem(name='new team')
    team_item.save()

    assert Team.objects.count() == before+1
