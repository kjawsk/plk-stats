# -*- coding: utf-8 -*-

import unittest
from stats_parser.spiders.starting_five import StartingFiveSpider
from responses import fake_response_from_file

class OsdirSpiderTest(unittest.TestCase):

    def setUp(self):
        self.spider = StartingFiveSpider()

    def _test_item_results(self, results, expected_length):
        count = 0
        permalinks = set()
        for item in results:
            self.assertIsNotNone(item['content'])
            self.assertIsNotNone(item['title'])
        self.assertEqual(count, expected_length)

    def test_parse(self):
        results = self.spider.parse(fake_response_from_file('samples/torun_wloclawek.html'))
        expected = {
            "teamB": [
                "Tyler Haws ", "Michał Chyliński", "Kamil Łączyński",
                "Fiodor Dmitriew", "Josip Sobin"
            ],
            "teamA": [
                "Krzysztof Sulima", "Obie Trotter", "Bartosz Diduszko",
                "Cheikh Mbodj", "Kyle Weaver"
                ]
        }
        self.assertEqual(results, expected)
