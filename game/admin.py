from django.contrib import admin
from .models import Player, Mission, MissionSubmission

@admin.register(Player)
class PlayerAdmin(admin.ModelAdmin):
    list_display = ('user', 'level', 'xp', 'health', 'streak')


@admin.register(Mission)
class MissionAdmin(admin.ModelAdmin):
    list_display = ('title', 'xp_reward')


@admin.action(description='Approve selected submissions and give XP')
def approve_selected_submissions(modeladmin, request, queryset):
    for submission in queryset:
        submission.approve_submission()


@admin.register(MissionSubmission)
class MissionSubmissionAdmin(admin.ModelAdmin):
    list_display = ('player', 'mission', 'status')
    list_filter = ('status',)
    actions = [approve_selected_submissions]