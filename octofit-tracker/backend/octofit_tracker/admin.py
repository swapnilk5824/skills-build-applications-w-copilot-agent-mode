from django.contrib import admin
from tracker.models import UserProfile, Team, TeamMember, Activity, Leaderboard, WorkoutSuggestion

admin.site.register(UserProfile)
admin.site.register(Team)
admin.site.register(TeamMember)
admin.site.register(Activity)
admin.site.register(Leaderboard)
admin.site.register(WorkoutSuggestion)
