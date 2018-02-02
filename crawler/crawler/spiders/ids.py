"""This is a module spider for scraping actions from matches
"""

# import scrapy
# import json
# import datetime;
# import re
#
# from crawler.items import MatchItem
# from stats.models import Team
#
# class IdsSpider(scrapy.Spider):
#
#     name = "ids"
#
#     def start_requests(self):
#         """Provides list of matches to scrap"""
#         start = 780133
#         amount = 10000
#         for match_id in range(start, start+amount):
#             url = "http://www.fibalivestats.com/data/%i/data.json" % match_id
#             yield scrapy.Request(url=url, callback=self.parse)
#
#
#     def parse(self, response):
#         data = json.loads(response.body_as_unicode())
#         home_team_name = data['tm']['1']['name']
#         away_team_name = data['tm']['2']['name']
#
#         try:
#             home_team = Team.objects.get(name=home_team_name)
#             away_team = Team.objects.get(name=away_team_name)
#         except Team.DoesNotExist:
#             pass
#         else:
#             match = MatchItem()
#             match['home_team'] = home_team
#             match['away_team'] = away_team
#             match['date'] = datetime.datetime.now()
#             match['fiba_id'] = re.search(r'\d+', response.url).group()
#             match.save()
#         finally:
#             self.logger.debug(
#                 "\n------\nHome team: %s\nAway team: %s\n" % (home_team_name, away_team_name)
#             )
