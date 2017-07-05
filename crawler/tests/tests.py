# -*- coding: utf-8 -*-

import unittest
import ast

import sys
sys.path.append('/home/karol/Projects/plkStats/page/')
import os
os.environ['DJANGO_SETTINGS_MODULE'] = 'page.settings'
import django
django.setup()

from crawler.spiders.starting_lineup import StartingLineupSpider
from crawler.spiders.play_by_play import PlayByPlaySpider
from responses import fake_response_from_file
from crawler.items import TeamItem
from stats.models import Team

class StartingLineupTest(unittest.TestCase):

    def setUp(self):
        self.spider = StartingLineupSpider()
        self.maxDiff = None

    def test_parse(self):
        results = self.spider.parse(fake_response_from_file('samples/torun_wloclawek.html'))
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
        self.assertEqual(results, expected)


class PlayByPlaySpiderTest(unittest.TestCase):

    def setUp(self):
        self.spider = PlayByPlaySpider()
        self.maxDiff = None

    def test_parse(self):
        results = self.spider.parse(
            fake_response_from_file('samples/torun_wloclawek.html')
        )

        path = "tests/responses/samples/play_by_play.txt"
        with open(path) as plays:
            for play in plays:
                result = next(results)
                play = play.replace("},", "}").strip()
                play = ast.literal_eval(play)
                self.assertEqual(play, result, msg="\nPlay: %s\nResult: %s" % (play, result))

class DjangoScrapyIntegrationTests(unittest.TestCase):

    def test_new_item_is_saved_in_db_through_django_orm(self):
        before = Team.objects.count()
        team_item = TeamItem(name='new team')
        team_item.save()

        self.assertEqual(Team.objects.count(), before+1)
