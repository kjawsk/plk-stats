from django.db import models

class Team(models.Model):
    name = models.CharField(max_length=50)

class Player(models.Model):
    name = models.CharField(max_length=100)
    team_id = models.ForeignKey(Team)

class Action_Type(models.Model):
    name = models.CharField(max_length=5)

class Match(models.Model):
    home_team = models.ForeignKey(Team, related_name='match_home_team')
    away_team = models.ForeignKey(Team, related_name='match_away_team')
    date = models.DateField(auto_now=False)

class Action(models.Model):
    match_id = models.ForeignKey(Match)
    action_type_id = models.ForeignKey(Action_Type)
    player_id = models.ForeignKey(Player)
    time = models.TimeField(auto_now=False)
