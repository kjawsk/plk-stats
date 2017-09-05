# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import re
import logging

from stats.models import Team, Player, Action_Type, Match, Action

class StatsParserPipeline(object):
        return item
