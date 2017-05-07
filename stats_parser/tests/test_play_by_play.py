# -*- coding: utf-8 -*-

import unittest
import ast
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

        path = "tests/responses/samples/play_by_play.txt"
        with open(path) as plays:
            for play in plays:
                result = next(results)
                play = play.replace("},", "}").strip()
                play = ast.literal_eval(play)
                self.assertEqual(play, result, msg="\nPlay: %s\nResult: %s" % (play, result))
