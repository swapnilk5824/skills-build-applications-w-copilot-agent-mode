from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from django.contrib.auth.models import User
from tracker.models import (
    UserProfile, Activity, Team,
    Leaderboard, WorkoutSuggestion
)
from tracker.serializers import (
    UserSerializer, UserProfileSerializer, ActivitySerializer,
    TeamSerializer, LeaderboardSerializer,
    WorkoutSuggestionSerializer
)


class UserViewSet(viewsets.ModelViewSet):
    """ViewSet for User model"""
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    @action(detail=True, methods=['get'])
    def profile(self, request, pk=None):
        """Get user profile"""
        user = self.get_object()
        profile = UserProfile.objects.get_or_create(user=user)[0]
        serializer = UserProfileSerializer(profile)
        return Response(serializer.data)


class UserProfileViewSet(viewsets.ModelViewSet):
    """ViewSet for UserProfile model"""
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]


class ActivityViewSet(viewsets.ModelViewSet):
    """ViewSet for Activity model"""
    queryset = Activity.objects.all()
    serializer_class = ActivitySerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        """Create activity and update user profile"""
        activity = serializer.save(user=self.request.user)
        profile = UserProfile.objects.get_or_create(user=self.request.user)[0]
        profile.total_workouts += 1
        profile.total_calories_burned += activity.calories_burned
        profile.save()
        
        # Update leaderboard
        leaderboard = Leaderboard.objects.get_or_create(user=self.request.user)[0]
        leaderboard.total_calories_burned += activity.calories_burned
        leaderboard.total_activities += 1
        leaderboard.save()

    def get_queryset(self):
        """Filter activities by user"""
        user = self.request.query_params.get('user', None)
        queryset = Activity.objects.all()
        if user:
            queryset = queryset.filter(user__username=user)
        return queryset


class TeamViewSet(viewsets.ModelViewSet):
    """ViewSet for Team model"""
    queryset = Team.objects.all()
    serializer_class = TeamSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        """Create team with current user as creator"""
        serializer.save(created_by=self.request.user)


class LeaderboardViewSet(viewsets.ReadOnlyModelViewSet):
    """ViewSet for Leaderboard model (Read-only)"""
    queryset = Leaderboard.objects.all()
    serializer_class = LeaderboardSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]


class WorkoutSuggestionViewSet(viewsets.ModelViewSet):
    """ViewSet for WorkoutSuggestion model"""
    queryset = WorkoutSuggestion.objects.all()
    serializer_class = WorkoutSuggestionSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        """Create workout suggestion for user"""
        if self.request.user.is_authenticated:
            serializer.save(user=self.request.user)
        else:
            serializer.save()

    def get_queryset(self):
        """Filter suggestions by user"""
        user = self.request.query_params.get('user', None)
        queryset = WorkoutSuggestion.objects.all()
        if user:
            queryset = queryset.filter(user__username=user)
        return queryset
