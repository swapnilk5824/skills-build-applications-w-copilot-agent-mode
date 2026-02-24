from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from tracker.models import (
    UserProfile, Activity, Team,
    Leaderboard, WorkoutSuggestion
)
from datetime import datetime, timedelta
from django.utils import timezone


class Command(BaseCommand):
    help = 'Populate the database with sample data'

    def handle(self, *args, **options):
        # Create sample users
        users_data = [
            {'username': 'john_fitness', 'email': 'john@example.com', 'first_name': 'John', 'last_name': 'Smith'},
            {'username': 'sarah_runner', 'email': 'sarah@example.com', 'first_name': 'Sarah', 'last_name': 'Johnson'},
            {'username': 'mike_gym', 'email': 'mike@example.com', 'first_name': 'Mike', 'last_name': 'Davis'},
            {'username': 'emma_yoga', 'email': 'emma@example.com', 'first_name': 'Emma', 'last_name': 'Wilson'},
            {'username': 'alex_cycling', 'email': 'alex@example.com', 'first_name': 'Alex', 'last_name': 'Brown'},
        ]

        users = []
        for user_data in users_data:
            user, created = User.objects.get_or_create(
                username=user_data['username'],
                defaults={
                    'email': user_data['email'],
                    'first_name': user_data['first_name'],
                    'last_name': user_data['last_name']
                }
            )
            users.append(user)
            if created:
                self.stdout.write(f'Created user: {user.username}')

        # Create user profiles
        for i, user in enumerate(users):
            profile, created = UserProfile.objects.get_or_create(
                user=user,
                defaults={
                    'bio': f'Fitness enthusiast {i+1}',
                    'fitness_level': ['beginner', 'intermediate', 'advanced'][i % 3],
                    'total_workouts': (i+1) * 5,
                    'total_calories_burned': (i+1) * 500
                }
            )
            if created:
                self.stdout.write(f'Created profile for: {user.username}')

        # Create teams
        teams_data = [
            {'name': 'Morning Runners', 'description': 'Early morning running group'},
            {'name': 'Gym Warriors', 'description': 'Strength and conditioning team'},
            {'name': 'Yoga Enthusiasts', 'description': 'Flexible and mindful group'},
        ]

        teams = []
        for team_data in teams_data:
            team, created = Team.objects.get_or_create(
                name=team_data['name'],
                defaults={
                    'description': team_data['description'],
                    'created_by': users[0],
                    'total_calories_burned': 0
                }
            )
            teams.append(team)
            if created:
                self.stdout.write(f'Created team: {team.name}')

        # Create activities
        activity_types = ['running', 'walking', 'cycling', 'swimming', 'gym', 'yoga']
        now = timezone.now()

        for user in users:
            for j in range(5):
                activity_type = activity_types[j % len(activity_types)]
                days_ago = j * 2
                
                activity, created = Activity.objects.get_or_create(
                    user=user,
                    activity_type=activity_type,
                    duration_minutes=30 + (j * 10),
                    logged_at=now - timedelta(days=days_ago),
                    defaults={
                        'calories_burned': 150 + (j * 25),
                        'distance_km': 5.0 + (j * 0.5),
                        'description': f'{activity_type.capitalize()} session',
                        'location': f'Location {j+1}'
                    }
                )
                if created:
                    self.stdout.write(f'Created activity for {user.username}: {activity_type}')

        # Create leaderboard entries
        for user in users:
            activities = Activity.objects.filter(user=user)
            total_calories = sum(a.calories_burned for a in activities)
            
            leaderboard, created = Leaderboard.objects.get_or_create(
                user=user,
                defaults={
                    'total_calories_burned': total_calories,
                    'total_activities': activities.count(),
                    'ranking': users.index(user) + 1
                }
            )
            if created:
                self.stdout.write(f'Created leaderboard entry for {user.username}')

        # Update rankings based on calories burned
        leaderboards = Leaderboard.objects.all().order_by('-total_calories_burned')
        for rank, leaderboard in enumerate(leaderboards, 1):
            leaderboard.ranking = rank
            leaderboard.save()

        # Create workout suggestions
        suggestions_data = [
            {'exercise_name': 'Morning Run', 'difficulty_level': 'intermediate', 'estimated_duration_minutes': 30, 'estimated_calories_burned': 250},
            {'exercise_name': 'Strength Training', 'difficulty_level': 'advanced', 'estimated_duration_minutes': 45, 'estimated_calories_burned': 350},
            {'exercise_name': 'Yoga Session', 'difficulty_level': 'beginner', 'estimated_duration_minutes': 60, 'estimated_calories_burned': 200},
            {'exercise_name': 'Cycling Tour', 'difficulty_level': 'intermediate', 'estimated_duration_minutes': 60, 'estimated_calories_burned': 400},
            {'exercise_name': 'Swimming', 'difficulty_level': 'advanced', 'estimated_duration_minutes': 45, 'estimated_calories_burned': 350},
        ]

        for user in users:
            for suggestion_data in suggestions_data:
                suggestion, created = WorkoutSuggestion.objects.get_or_create(
                    user=user,
                    exercise_name=suggestion_data['exercise_name'],
                    defaults={
                        'description': f"Try this {suggestion_data['exercise_name'].lower()} to improve fitness",
                        'difficulty_level': suggestion_data['difficulty_level'],
                        'estimated_duration_minutes': suggestion_data['estimated_duration_minutes'],
                        'estimated_calories_burned': suggestion_data['estimated_calories_burned'],
                        'is_completed': False
                    }
                )
                if created:
                    self.stdout.write(f'Created suggestion for {user.username}: {suggestion_data["exercise_name"]}')

        self.stdout.write(self.style.SUCCESS('Successfully populated the database!'))
