"""This module is implementation of self test functionallity. Each match website constains
table with summary statistics for each team. It could be used to make a test to check if data
stored in database by spider is in line with offical statistics
"""

import re
import datetime
import logging
from collections import namedtuple

from django.db.models import Q
from stats.models import Action, Action_Type, Player, Team
from crawler.utils.xpaths import x_stats

class SelfTest:
    """This class is responsible for comparing data fetched by spiders and data from statistics
    tablefrom scraped website
    """

    def __init__(self, response, match):
        self.match = match
        self.response = response

    def _extract_throws(self, xpath):
        extracted = self.response.xpath(xpath).extract()
        throws = re.search(r"\d+/\d+", "".join(extracted)).group()
        if not throws:
            logger.critical("Throws not found in: %s" % (extracted))
            raise ValueError
        succ = int(throws.split("/")[0])
        all_ = int(throws.split("/")[1])
        return dict(succ=succ, all=all_)

    def run(self):
        """Logic flow:
        TBD
        """
        logger = logging.getLogger('selftest')
        logger.debug("Seltest started")

        home_scraped_throws = dict()
        home_expected_throws = self._extract_throws(x_stats["home"]["2PKT"])
        home_scraped_throws["succ"] = Action.objects.filter(
            action_type__name="C2PKT",
            match=self.match,
            player__team=self.match.home_team).count()
        home_scraped_throws["all"] = Action.objects.filter(
            Q(action_type__name="N2PKT")|Q(action_type__name="Z2PKT")|Q(action_type__name="C2PKT"),
            match=self.match,
            player__team=self.match.home_team).count()

        if home_scraped_throws["succ"] != home_expected_throws["succ"]:
            logger.critical(
                "Success 2 pkt throws of home team - data is inconsistent with stats: %s %s" %
                (home_scraped_throws["succ"], home_expected_throws["succ"]))

        if home_scraped_throws["all"] != home_expected_throws["all"]:
            logger.critical(
                "All 2 pkt throws of home team - data is inconsistent with stats %s %s" %
                (home_scraped_throws["all"], home_expected_throws["all"]))

        away_scraped_throws = dict()
        away_expected_throws = self._extract_throws(x_stats["away"]["2PKT"])
        away_scraped_throws["succ"] = Action.objects.filter(
            action_type__name="C2PKT",
            match=self.match,
            player__team=self.match.away_team).count()
        away_scraped_throws["all"] = Action.objects.filter(
            Q(action_type__name="N2PKT")|Q(action_type__name="Z2PKT")|Q(action_type__name="C2PKT"),
            match=self.match,
            player__team=self.match.away_team).count()

        if away_scraped_throws["succ"] != away_expected_throws["succ"]:
            logger.critical(
                "Success 2 pkt throws of away team - data is inconsistent with stats %s %s" %
                (away_scraped_throws["succ"], away_expected_throws["succ"]))

        if away_scraped_throws["all"] != away_expected_throws["all"]:
            logger.critical(
                "All 2 pkt throws of away team - data is inconsistent with stats %s %s" %
                (away_scraped_throws["all"], away_expected_throws["all"]))

        logger.debug("Seltest finished")
