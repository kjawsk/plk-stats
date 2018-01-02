from django.db import models

class Team(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

class Player(models.Model):
    name = models.CharField(max_length=100)
    short_name = models.CharField(max_length=1)
    team = models.ForeignKey(Team)
    passport = models.CharField(max_length=30)
    birth = models.DateField(auto_now=False)
    height = models.PositiveIntegerField()
    position = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Action_Type(models.Model):
    name = models.CharField(max_length=20)

    def __str__(self):
        return self.name

class Action_Subtype(models.Model):
    name = models.CharField(max_length=20)

    def __str__(self):
        return self.name

class Period_Type(models.Model):
    name = models.CharField(max_length=8)

    def __str__(self):
        return self.name

class Match(models.Model):
    home_team = models.ForeignKey(Team, related_name='match_home_team')
    away_team = models.ForeignKey(Team, related_name='match_away_team')
    date = models.DateField(auto_now=False)
    fiba_id = models.IntegerField()

    def __str__(self):
        return ("%s: %s - %s") % (self.date, self.home_team.name, self.away_team.name)

class Action(models.Model):
    match = models.ForeignKey(Match)
    team = models.ForeignKey(Team)
    action_type = models.ForeignKey(Action_Type)
    action_subtype = models.ForeignKey(Action_Subtype, null=True)
    player = models.ForeignKey(Player, null=True)
    time = models.TimeField(auto_now=False)
    success = models.BooleanField()
    period_type = models.ForeignKey(Period_Type)
    period = models.PositiveIntegerField()

    def __str__(self):
        return ("%s: %s %s") % (self.time, self.player.name, self.action_type.name)
