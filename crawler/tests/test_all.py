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

from crawler.spiders.starting_lineup import StartingLineupSpider
from crawler.spiders.play_by_play import PlayByPlaySpider
from crawler.items import TeamItem
from stats.models import Team, Action
from .responses import fake_response_from_file

def test_starting_lineup_spider():
    """Test for starting lineup spider, fake response is used"""
    spider = StartingLineupSpider()
    results = spider.parse(fake_response_from_file('samples/torun_wloclawek.html'))
    expected = {
        "away_bench": ["Toney McCray", "Rafał Komenda", "Nemanja Jaramaz", "Mateusz Bartosz",
            "James Washington", "Paweł Leończyk", "Kacper Młynarski"],
        "away_s5": ["Tyler Haws", "Michał Chyliński", "Kamil Łączyński", "Fiodor Dmitriew",
            "Josip Sobin"],
        "away_team_name": ["Anwil Włocławek"],
        "date": "23.04.2017",
        "home_bench": ["Kacper Lambarski", "Tomasz Gałan", "Tomasz Śnieg", "Kamil Michalski",
            "Jure Škifić", "Maksym Sanduł", "Aleksander Perka"],
        "home_s5": ["Krzysztof Sulima", "Obie Trotter", "Bartosz Diduszko", "Cheikh Mbodj",
            "Kyle Weaver"],
        "home_team_name": ['Polski Cukier Toruń']
    }
    assert results == expected

def test_play_by_play_spider():
    """Test for play by play spider, fake response is used(look into responses folder), result is
    compared with prepared expected result. It is used for refactoring"""
    spider = PlayByPlaySpider()
    results = spider.parse(
        fake_response_from_file('samples/torun_wloclawek.html')
    )

    path = "tests/responses/samples/play_by_play.txt"
    with open(path) as plays:
        for play in plays:
            result = next(results)
            play = play.replace("},", "}").strip()
            play = ast.literal_eval(play)
            assert play == result

def test_item_is_saved_in_db():
    """Test for scrapy - django orm integration"""
    before = Team.objects.count()
    team_item = TeamItem(name='new team')
    team_item.save()

    assert Team.objects.count() == before+1

def test_action_is_parsed():
    """Test for action pipeline"""
    assert 1
