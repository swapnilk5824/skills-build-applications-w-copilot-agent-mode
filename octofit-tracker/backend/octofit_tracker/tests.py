from django.test import TestCase
from django.contrib.auth.models import User
from tracker.models import UserProfile, Team, Activity, Leaderboard, WorkoutSuggestion

class UserProfileTest(TestCase):
    def test_create_user_profile(self):
        user = User.objects.create(username='testuser', email='test@example.com')
        profile = UserProfile.objects.create(user=user, fitness_level='beginner')
        self.assertEqual(profile.user.username, 'testuser')

class TeamTest(TestCase):
    def test_create_team(self):
        user = User.objects.create(username='creator')
        team = Team.objects.create(name='Test Team', created_by=user)
        self.assertEqual(team.name, 'Test Team')

class ActivityTest(TestCase):
    def test_create_activity(self):
        user = User.objects.create(username='activityuser')
        activity = Activity.objects.create(user=user, activity_type='running', duration_minutes=30, calories_burned=100)
        self.assertEqual(activity.activity_type, 'running')

class LeaderboardTest(TestCase):
    def test_create_leaderboard(self):
        user = User.objects.create(username='leaderboarduser')
        leaderboard = Leaderboard.objects.create(user=user, total_calories_burned=500, total_activities=5, ranking=1)
        self.assertEqual(leaderboard.ranking, 1)

class WorkoutSuggestionTest(TestCase):
    def test_create_workout_suggestion(self):
        user = User.objects.create(username='workoutuser')
        suggestion = WorkoutSuggestion.objects.create(user=user, exercise_name='Test Workout', difficulty_level='beginner', estimated_duration_minutes=20, estimated_calories_burned=100)
        self.assertEqual(suggestion.exercise_name, 'Test Workout')
