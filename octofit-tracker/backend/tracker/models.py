from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class UserProfile(models.Model):
    """Extended user profile with fitness tracking information"""
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    bio = models.TextField(blank=True, null=True)
    profile_picture = models.URLField(blank=True, null=True)
    fitness_level = models.CharField(
        max_length=20,
        choices=[
            ('beginner', 'Beginner'),
            ('intermediate', 'Intermediate'),
            ('advanced', 'Advanced'),
        ],
        default='beginner'
    )
    total_workouts = models.IntegerField(default=0)
    total_calories_burned = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username} Profile"


class Team(models.Model):
    """Team model for group fitness challenges"""
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_teams')
    total_calories_burned = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class TeamMember(models.Model):
    """Through model for Team and User relationship"""
    team = models.ForeignKey(Team, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    joined_at = models.DateTimeField(auto_now_add=True)
    calories_burned = models.IntegerField(default=0)

    class Meta:
        unique_together = ('team', 'user')

    def __str__(self):
        return f"{self.user.username} in {self.team.name}"


class Activity(models.Model):
    """Activity logging model for tracking exercises"""
    ACTIVITY_TYPES = [
        ('running', 'Running'),
        ('walking', 'Walking'),
        ('cycling', 'Cycling'),
        ('swimming', 'Swimming'),
        ('gym', 'Gym'),
        ('yoga', 'Yoga'),
        ('sports', 'Sports'),
        ('other', 'Other'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='activities')
    activity_type = models.CharField(max_length=20, choices=ACTIVITY_TYPES)
    duration_minutes = models.IntegerField()
    calories_burned = models.IntegerField()
    distance_km = models.FloatField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    location = models.CharField(max_length=100, blank=True, null=True)
    logged_at = models.DateTimeField(default=timezone.now)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.activity_type}"

    class Meta:
        ordering = ['-logged_at']


class Leaderboard(models.Model):
    """Leaderboard model for tracking rankings"""
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='leaderboard')
    total_calories_burned = models.IntegerField(default=0)
    total_activities = models.IntegerField(default=0)
    ranking = models.IntegerField(default=0)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username} - Rank #{self.ranking}"

    class Meta:
        ordering = ['ranking']


class WorkoutSuggestion(models.Model):
    """Personalized workout suggestions based on user profile"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='workout_suggestions')
    exercise_name = models.CharField(max_length=100)
    description = models.TextField()
    difficulty_level = models.CharField(
        max_length=20,
        choices=[
            ('beginner', 'Beginner'),
            ('intermediate', 'Intermediate'),
            ('advanced', 'Advanced'),
        ]
    )
    estimated_duration_minutes = models.IntegerField()
    estimated_calories_burned = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_completed = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.exercise_name} for {self.user.username}"

    class Meta:
        ordering = ['-created_at']
