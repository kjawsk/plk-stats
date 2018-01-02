# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

from scrapy_djangoitem import DjangoItem
from stats.models import Action, Action_Type, Action_Subtype, Match, Team, Player

class MatchItem(DjangoItem):
    django_model = Match

class TeamItem(DjangoItem):
    django_model = Team

class ActionItem(DjangoItem):
    django_model = Action

class ActionTypeItem(DjangoItem):
    django_model = Action_Type

class ActionSubtypeItem(DjangoItem):
    django_model = Action_Subtype

class PlayerItem(DjangoItem):
    django_model = Player
