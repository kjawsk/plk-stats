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
from crawler.utils.xpaths import x_home_team_2pkt_throws, x_away_team_2pkt_throws

class SelfTest:
    """This class is responsible for comparing data fetched by spiders and data from statistics
    tablefrom scraped website
    """

    Throws = namedtuple('Throws', ['succ', 'all'])

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
        return self.Throws(succ=succ, all=all_)

    def run(self):
        """Logic flow:
        TBD
        """
        logger = logging.getLogger('selftest')
        logger.debug("Seltest started")

        home_2pkt_throws = self._extract_throws(x_home_team_2pkt_throws)
        away_2pkt_throws = self._extract_throws(x_away_team_2pkt_throws)

        expected_home_succ_2pkt = Action.objects.filter(
            match=self.match,
            player__team=self.match.home_team,
            action_type__name="C2PKT").count()
        expected_home_all_2pkt = Action.objects.filter(
            Q(action_type__name="N2PKT")|Q(action_type__name="Z2PKT")|Q(action_type__name="C2PKT"),
            match=self.match,
            player__team=self.match.home_team).count()

        if home_2pkt_throws.succ != expected_home_succ_2pkt:
            logger.critical(
                "Success 2 pkt throws of home team - data is inconsistent with stats: %s %s" %
                (home_2pkt_throws.succ, expected_home_succ_2pkt))

        if home_2pkt_throws.all != expected_home_all_2pkt:
            logger.critical(
                "All 2 pkt throws of home team - data is inconsistent with stats %s %s" %
                (home_2pkt_throws.all, expected_home_all_2pkt))

        expected_away_succ_2pkt = Action.objects.filter(
            match=self.match,
            player__team=self.match.away_team,
            action_type__name="C2PKT").count()
        expected_away_all_2pkt = Action.objects.filter(
            Q(action_type__name="N2PKT")|Q(action_type__name="Z2PKT")|Q(action_type__name="C2PKT"),
            match=self.match,
            player__team=self.match.away_team).count()

        if away_2pkt_throws.succ != expected_away_succ_2pkt:
            logger.critical(
                "Success 2 pkt throws of away team - data is inconsistent with stats %s %s" %
                (away_2pkt_throws.succ, expected_away_succ_2pkt))

        if away_2pkt_throws.all != expected_away_all_2pkt:
            logger.critical(
                "All 2 pkt throws of away team - data is inconsistent with stats %s %s" %
                (away_2pkt_throws.all, expected_away_all_2pkt))

        logger.debug("Seltest finished")
