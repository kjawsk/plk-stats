"""This module is implementation of self test functionallity. Each match website constains
table with summary statistics for each team. It could be used to make a test to check if data
stored in database by spider is in line with offical statistics
"""

import re
import datetime
import logging

from django.db.models import Q
from stats.models import Action, Action_Type, Player, Team
from crawler.utils.xpaths import x_home_team_2pkt_throws, x_away_team_2pkt_throws

class SelfTest:
    """This class is responsible for comparing data fetched by spiders and data from statistics
    tablefrom scraped website
    """

    @classmethod
    def run(self, response, match):
        """Logic flow:
        1. Get number of successful throws from stats table
        2. Get number of all throws from stats table
        3. Compare numbers from 1. and 2. with data stored in database by spider
        """
        logger = logging.getLogger('selftest')
        logger.debug("Seltest started")

        extracted = response.xpath(x_home_team_2pkt_throws).extract()
        home_team_throws = re.search(r"\d+/\d+", "".join(extracted)).group()
        if not home_team_throws:
            logger.critical("%s %s" % (extracted, home_team_throws))
            return
        home_succ_2pkt = home_team_throws.split("/")[0]
        home_all_2pkt = home_team_throws.split("/")[1]

        extracted = response.xpath(x_away_team_2pkt_throws).extract()
        away_team_throws = re.search(r"\d+/\d+", "".join(extracted)).group()
        if not away_team_throws:
            logger.critical("%s %s" % (extracted, away_team_throws))
            return
        away_succ_2pkt = away_team_throws.split("/")[0]
        away_all_2pkt = away_team_throws.split("/")[1]

        expected_succ_2pkt = Action.objects.filter(match=match, action_type__name="C2PKT").count()
        expected_all_2pkt = Action.objects.filter(
            Q(action_type__name="N2PKT") | Q(action_type__name="Z2PKT"), match=match
        ).count()

        all_success_throws = int(home_succ_2pkt)+int(away_succ_2pkt)
        if all_success_throws != expected_succ_2pkt:
            logger.critical("Success 2 pkt throws - data is inconsistent with stats")

        all_no_success_throws = \
            int(home_all_2pkt)-int(home_succ_2pkt)+int(away_all_2pkt)-int(away_succ_2pkt)
        if all_no_success_throws != expected_all_2pkt:
            logger.critical("No success 2 pkt throws - data is inconsistent with stats")

        logger.debug("Seltest finished")
