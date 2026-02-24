from rest_framework import serializers
from django.contrib.auth.models import User
from tracker.models import (
    UserProfile, Activity, Team, TeamMember,
    Leaderboard, WorkoutSuggestion
)


class UserSerializer(serializers.ModelSerializer):
    """Serializer for User model - converts ObjectId fields to strings"""
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name']
        read_only_fields = ['id']


class UserProfileSerializer(serializers.ModelSerializer):
    """Serializer for UserProfile model"""
    user = UserSerializer(read_only=True)

    class Meta:
        model = UserProfile
        fields = ['id', 'user', 'bio', 'profile_picture', 'fitness_level',
                  'total_workouts', 'total_calories_burned', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']


class ActivitySerializer(serializers.ModelSerializer):
    """Serializer for Activity model"""
    user = UserSerializer(read_only=True)

    class Meta:
        model = Activity
        fields = ['id', 'user', 'activity_type', 'duration_minutes', 'calories_burned',
                  'distance_km', 'description', 'location', 'logged_at', 'created_at']
        read_only_fields = ['id', 'created_at']


class TeamMemberSerializer(serializers.ModelSerializer):
    """Serializer for TeamMember model"""
    user = UserSerializer(read_only=True)

    class Meta:
        model = TeamMember
        fields = ['id', 'user', 'joined_at', 'calories_burned']
        read_only_fields = ['id', 'joined_at']


class TeamSerializer(serializers.ModelSerializer):
    """Serializer for Team model"""
    created_by = UserSerializer(read_only=True)

    class Meta:
        model = Team
        fields = ['id', 'name', 'description', 'created_by',
                  'total_calories_burned', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']


class LeaderboardSerializer(serializers.ModelSerializer):
    """Serializer for Leaderboard model"""
    user = UserSerializer(read_only=True)

    class Meta:
        model = Leaderboard
        fields = ['id', 'user', 'total_calories_burned', 'total_activities', 'ranking', 'updated_at']
        read_only_fields = ['id', 'updated_at']


class WorkoutSuggestionSerializer(serializers.ModelSerializer):
    """Serializer for WorkoutSuggestion model"""
    user = UserSerializer(read_only=True)

    class Meta:
        model = WorkoutSuggestion
        fields = ['id', 'user', 'exercise_name', 'description', 'difficulty_level',
                  'estimated_duration_minutes', 'estimated_calories_burned',
                  'created_at', 'is_completed']
        read_only_fields = ['id', 'created_at']
