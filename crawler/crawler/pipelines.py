# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import re
import logging

from stats.models import Team, Player, Action_Type, Match, Action

class StatsParserPipeline(object):
    def process_item(self, item, spider):
        if "celny" in item["action"] and "2 pkt" in item["action"] and "niecelny" not in item["action"]:
            player_name = re.match(r"\w+\.+\s+[\w]+", item["action"]).group()
            try:
                player_id = Player.objects.get(name=player_name)
            except Player.DoesNotExist:
                logger = logging.getLogger('plkStats')
                logger.setLevel(logging.DEBUG)
                # create file handler which logs even debug messages
                fh = logging.FileHandler('logs/pipelines.log')
                fh.setLevel(logging.DEBUG)
                # create formatter and add it to the handlers
                formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
                fh.setFormatter(formatter)
                # add the handlers to the logger
                logger.addHandler(fh)
                logger.info("Player name %s from following action not found in database. Time: %s" % (player_name, item["time"]))
            else:
                action = Action(
                    match_id=Match.objects.first(),
                    action_type_id=Action_Type.objects.get(name="C2PKT"),
                    player_id=player_id,
                    time=item["time"]
                )
                action.save()
        elif ("niecelny" in item["action"] or "zablokowany" in item["action"]) and "2 pkt" in item["action"]:
            player_name = re.match(r"\w+\.+\s+[\w]+", item["action"]).group()
            try:
                player_id = Player.objects.get(name=player_name)
            except Player.DoesNotExist:
                logger = logging.getLogger('plkStats')
                logger.setLevel(logging.DEBUG)
                # create file handler which logs even debug messages
                fh = logging.FileHandler('logs/pipelines.log')
                fh.setLevel(logging.DEBUG)
                # create formatter and add it to the handlers
                formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
                fh.setFormatter(formatter)
                # add the handlers to the logger
                logger.addHandler(fh)
                logger.info("Player name %s from following action not found in database. Time: %s" % (player_name, item["time"]))
            else:
                action = Action(
                    match_id=Match.objects.first(),
                    action_type_id=Action_Type.objects.get(name="N2PKT"),
                    player_id=player_id,
                    time=item["time"]
                    )
                action.save()

        return item
