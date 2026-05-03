from django.contrib import admin
from .models import Player, Mission

@admin.register(Player)
class PlayerAdmin(admin.ModelAdmin):
    list_display = ('user', 'level', 'xp', 'health', 'streak')


@admin.action(description='Approve selected missions and give XP')
def approve_selected_missions(modeladmin, request, queryset):
    for mission in queryset:
        mission.approve_mission()


@admin.register(Mission)
class MissionAdmin(admin.ModelAdmin):
    list_display = ('title', 'player', 'xp_reward', 'status')
    list_filter = ('status',)
    search_fields = ('title', 'player__user__username')
    actions = [approve_selected_missions]