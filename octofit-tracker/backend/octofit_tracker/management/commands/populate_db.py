from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from tracker.models import (
    UserProfile, Activity, Team, Leaderboard, WorkoutSuggestion
)
from django.utils import timezone

class Command(BaseCommand):
    help = 'Populate the octofit_db database with test data'

    def handle(self, *args, **options):
        # Clear all data
        User.objects.all().delete()
        UserProfile.objects.all().delete()
        Activity.objects.all().delete()
        Team.objects.all().delete()
        Leaderboard.objects.all().delete()
        WorkoutSuggestion.objects.all().delete()

        # Create super hero users
        users_data = [
            {'username': 'ironman', 'email': 'ironman@marvel.com', 'first_name': 'Tony', 'last_name': 'Stark'},
            {'username': 'spiderman', 'email': 'spiderman@marvel.com', 'first_name': 'Peter', 'last_name': 'Parker'},
            {'username': 'batman', 'email': 'batman@dc.com', 'first_name': 'Bruce', 'last_name': 'Wayne'},
            {'username': 'wonderwoman', 'email': 'wonderwoman@dc.com', 'first_name': 'Diana', 'last_name': 'Prince'},
        ]
        users = []
        for user_data in users_data:
            user = User.objects.create(**user_data)
            users.append(user)

        # Create teams
        marvel = Team.objects.create(name='Marvel', description='Marvel Superheroes', created_by=users[0])
        dc = Team.objects.create(name='DC', description='DC Superheroes', created_by=users[2])

        # Create user profiles
        for user in users:
            UserProfile.objects.create(user=user, bio=f'{user.username} is a superhero!', fitness_level='advanced', total_workouts=10, total_calories_burned=1000)

        # Create activities
        for user in users:
            Activity.objects.create(user=user, activity_type='running', duration_minutes=30, calories_burned=300, description='Morning run', location='City', logged_at=timezone.now())
            Activity.objects.create(user=user, activity_type='gym', duration_minutes=60, calories_burned=500, description='Gym session', location='HQ', logged_at=timezone.now())

        # Create leaderboard
        for i, user in enumerate(users):
            Leaderboard.objects.create(user=user, total_calories_burned=800 + i*100, total_activities=2, ranking=i+1)

        # Create workout suggestions
        for user in users:
            WorkoutSuggestion.objects.create(user=user, exercise_name='Hero Training', description='Intense superhero workout', difficulty_level='advanced', estimated_duration_minutes=60, estimated_calories_burned=600, is_completed=False)

        self.stdout.write(self.style.SUCCESS('Successfully populated octofit_db with superhero test data!'))
