from django.contrib import admin
from .models import Team, Player, Action_Type, Action_Subtype, Match, Action, Period_Type

class TeamAdminSite(admin.ModelAdmin):
    model = Team
    list_display = ('name',)


class PlayerAdminSite(admin.ModelAdmin):
    model = Player
    list_display = (
        'name',
        'get_team_name',
    )

    def get_team_name(self, obj):
        return obj.team.name

    get_team_name.short_description = 'Team'

class ActionTypeAdminSite(admin.ModelAdmin):
    model = Action_Type
    list_display = ('name',)

class ActionSubtypeAdminSite(admin.ModelAdmin):
    model = Action_Subtype
    list_display = ('name', )

class MatchAdminSite(admin.ModelAdmin):
    model = Match

class PeriodTypeSite(admin.ModelAdmin):
    model = Period_Type

class ActionAdminSite(admin.ModelAdmin):
    model = Action
    list_display = (
        'get_player_name',
        'get_action_name',
        'get_time',
        'success',
        'period_type'
    )

    def get_player_name(self, obj):
        return obj.player.name

    def get_action_name(self, obj):
        return obj.action_type.name

    def get_time(self, obj):
        return obj.time.strftime("%M:%S")

    get_action_name.short_description = 'Action'
    get_player_name.short_description = 'Player'
    get_time.short_description = 'Time'

admin.site.register(Team, TeamAdminSite)
admin.site.register(Player, PlayerAdminSite)
admin.site.register(Action_Type, ActionTypeAdminSite)
admin.site.register(Action_Subtype, ActionSubtypeAdminSite)
admin.site.register(Match, MatchAdminSite)
admin.site.register(Action, ActionAdminSite)
admin.site.register(Period_Type, PeriodTypeSite)
