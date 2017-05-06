# -*- coding: utf-8 -*-

import unittest
from stats_parser.spiders.play_by_play import PlayByPlaySpider
from responses import fake_response_from_file

class StartingLineupTest(unittest.TestCase):

    def setUp(self):
        self.spider = PlayByPlaySpider()
        self.maxDiff = None

    def test_parse(self):
        results = self.spider.parse(
            fake_response_from_file('samples/torun_wloclawek.html')
        )
        expected = {
            "team":"away",
            "time":"09:42",
            "action":"F. Dmitriew - faul osobisty (1 F, 1 Faul zespołu). Faulowany: K. Sulima",
        }
        self.assertEqual(next(results), expected)

        expected = {
            "team":"home",
            "time":"09:32",
            "action":"K. Sulima - celny lay-up za 2 pkt (2 Pkt). K. Weaver - asysta (1 AS)",
        }
        self.assertEqual(next(results), expected)
