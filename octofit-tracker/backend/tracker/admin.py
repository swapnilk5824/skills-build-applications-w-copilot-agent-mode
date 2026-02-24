from django.contrib import admin
from tracker.models import (
    UserProfile, Activity, Team,
    Leaderboard, WorkoutSuggestion
)


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'fitness_level', 'total_workouts', 'total_calories_burned')
    list_filter = ('fitness_level', 'created_at')
    search_fields = ('user__username',)


@admin.register(Activity)
class ActivityAdmin(admin.ModelAdmin):
    list_display = ('user', 'activity_type', 'duration_minutes', 'calories_burned', 'logged_at')
    list_filter = ('activity_type', 'logged_at')
    search_fields = ('user__username', 'description')


@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):
    list_display = ('name', 'created_by', 'total_calories_burned', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('name', 'created_by__username')


@admin.register(Leaderboard)
class LeaderboardAdmin(admin.ModelAdmin):
    list_display = ('user', 'ranking', 'total_calories_burned', 'total_activities')
    list_filter = ('ranking',)
    search_fields = ('user__username',)


@admin.register(WorkoutSuggestion)
class WorkoutSuggestionAdmin(admin.ModelAdmin):
    list_display = ('exercise_name', 'user', 'difficulty_level', 'is_completed', 'created_at')
    list_filter = ('difficulty_level', 'is_completed', 'created_at')
    search_fields = ('exercise_name', 'user__username')
