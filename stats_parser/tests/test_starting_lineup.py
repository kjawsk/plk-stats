# -*- coding: utf-8 -*-

import unittest
from stats_parser.spiders.starting_lineup import StartingLineupSpider
from responses import fake_response_from_file

class StartingLineupTest(unittest.TestCase):

    def setUp(self):
        self.spider = StartingLineupSpider()
        self.maxDiff = None

    def test_parse(self):
        results = self.spider.parse(fake_response_from_file('samples/torun_wloclawek.html'))
        expected = {
            "Polski Cukier Toruń":{
                "starting":["Krzysztof Sulima", "Obie Trotter", "Bartosz Diduszko", "Cheikh Mbodj", "Kyle Weaver"],
                "bench":["Kacper Lambarski", "Tomasz Gałan", "Tomasz Śnieg", "Kamil Michalski", "Jure Škifić", "Maksym Sanduł", "Aleksander Perka"],
            },
            "Anwil Włocławek":{
                "starting":["Tyler Haws", "Michał Chyliński", "Kamil Łączyński", "Fiodor Dmitriew", "Josip Sobin"],
                "bench":["Toney McCray", "Rafał Komenda", "Nemanja Jaramaz", "Mateusz Bartosz", "James Washington", "Paweł Leończyk", "Kacper Młynarski"],
            },
        }
        self.assertEqual(results, expected)
