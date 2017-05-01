# -*- coding: utf-8 -*-

import unittest
from stats_parser.spiders.starting_five import StartingFiveSpider
from responses import fake_response_from_file

class StartingFiveSpiderTest(unittest.TestCase):

    def setUp(self):
        self.spider = StartingFiveSpider()

    def test_parse(self):
        results = self.spider.parse(fake_response_from_file('samples/torun_wloclawek.html'))
        expected = {
            "Anwil Włocławek": [
                "Tyler Haws ", "Michał Chyliński", "Kamil Łączyński",
                "Fiodor Dmitriew", "Josip Sobin"
            ],
            "Polski Cukier Toruń": [
                "Krzysztof Sulima", "Obie Trotter", "Bartosz Diduszko",
                "Cheikh Mbodj", "Kyle Weaver"
                ]
        }
        self.assertEqual(results, expected)
