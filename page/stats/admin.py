from django.contrib import admin
from .models import Team, Player, Action_Type

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
        return obj.team_id.name

    get_team_name.short_description = 'Team'

class ActionTypeAdminSite(admin.ModelAdmin):
    model = Action_Type
    list_display = ('name',)

admin.site.register(Team, TeamAdminSite)
admin.site.register(Player, PlayerAdminSite)
admin.site.register(Action_Type, ActionTypeAdminSite)
