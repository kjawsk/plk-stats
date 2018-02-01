# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class PlayerItem(scrapy.Item):

    name = scrapy.Field()
    short_name = scrapy.Field()
    passport = scrapy.Field()
    birth = scrapy.Field()
    height = scrapy.Field()
    position = scrapy.Field()


class TeamPlayersItem(scrapy.Item):
    team_name = scrapy.Field()
    current_players = scrapy.Field()
    past_players = scrapy.Field()