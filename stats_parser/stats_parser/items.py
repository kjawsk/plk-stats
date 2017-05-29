# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy
import re

def remove_whitespaces(buff):
    result = list(map(str.split, buff))
    result = [' '.join(x) for x in result]
    return result

def extract_date(buff):
    return re.search(r'(\d+.\d+.\d+)', buff[2]).group(1)

class MatchItem(scrapy.Item):
    home_team_name = scrapy.Field(output_processor=remove_whitespaces)
    away_team_name = scrapy.Field(output_processor=remove_whitespaces)
    home_s5 = scrapy.Field(output_processor=remove_whitespaces)
    away_s5 = scrapy.Field(output_processor=remove_whitespaces)
    home_bench = scrapy.Field(output_processor=remove_whitespaces)
    away_bench = scrapy.Field(output_processor=remove_whitespaces)
    date = scrapy.Field(output_processor=extract_date)

class ActionItem(scrapy.Item):
    action_type = scrapy.Field(output_processor=remove_whitespaces)
    time = scrapy.Field(output_processor=remove_whitespaces)
