# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

from scrapy_djangoitem import DjangoItem
from stats.models import Action, Match, Team

class MatchItem(DjangoItem):
    django_model = Match

class TeamItem(DjangoItem):
    django_model = Team

class ActionItem(DjangoItem):
    django_model = Action
