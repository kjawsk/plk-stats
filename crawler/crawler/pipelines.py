# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import re

from stats.models import Team, Player, Action_Type, Match, Action

class StatsParserPipeline(object):
    def process_item(self, item, spider):
        try:
            # first letter of name, dot and space are omitted by [3:]
            player_name = re.match(r"\w\.+\s+['A-Za-z]+", item["action"]).group()[3:]
        except:
            player_name = None

        if "celny" in item["action"] and "2 pkt" in item["action"] and player_name:
            action = Action(
                match_id=Match.objects.first(),
                action_type_id=Action_Type.objects.get(name="C2PKT"),
                player_id=Player.objects.get(name=player_name),
                time=item["time"]
            )
            action.save()

        return item
