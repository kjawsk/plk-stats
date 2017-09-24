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
        succ = throws.split("/")[0]
        all_ = throws.split("/")[1]
        return self.Throws(succ=succ, all=all_)

    def run(self):
        """Logic flow:
        1. Get number of successful throws from stats table
        2. Get number of all throws from stats table
        3. Compare numbers from 1. and 2. with data stored in database by spider
        """
        logger = logging.getLogger('selftest')
        logger.debug("Seltest started")

        home_2pkt_throws = self._extract_throws(x_home_team_2pkt_throws)
        away_2pkt_throws = self._extract_throws(x_away_team_2pkt_throws)

        expected_succ_2pkt = Action.objects.filter(
            match=self.match,
            action_type__name="C2PKT").count()
        expected_all_2pkt = Action.objects.filter(
            Q(action_type__name="N2PKT") | Q(action_type__name="Z2PKT"),
            match=self.match).count()

        all_success_throws = int(home_2pkt_throws.succ)+int(away_2pkt_throws.succ)
        if all_success_throws != expected_succ_2pkt:
            logger.critical("Success 2 pkt throws - data is inconsistent with stats")

        all_no_success_throws = \
            int(home_2pkt_throws.all)-int(home_2pkt_throws.succ)+\
            int(away_2pkt_throws.all)-int(away_2pkt_throws.succ)
        if all_no_success_throws != expected_all_2pkt:
            logger.critical("No success 2 pkt throws - data is inconsistent with stats")

        logger.debug("Seltest finished")
