# -*- coding: utf-8 -*-

import unittest
from crawler.spiders.starting_lineup import StartingLineupSpider
from responses import fake_response_from_file

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
