import os
from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework.response import Response
from rest_framework.decorators import api_view
from tracker import views

codespace_name = os.environ.get('CODESPACE_NAME')
if codespace_name:
    base_url = f"https://{codespace_name}-8000.app.github.dev"
else:
    base_url = "http://localhost:8000"

router = DefaultRouter()
router.register(r'users', views.UserViewSet)
router.register(r'profiles', views.UserProfileViewSet)
router.register(r'activities', views.ActivityViewSet)
router.register(r'teams', views.TeamViewSet)
router.register(r'leaderboards', views.LeaderboardViewSet)
router.register(r'workouts', views.WorkoutSuggestionViewSet)

@api_view(['GET'])
def api_root(request):
    return Response({
        'users': request.build_absolute_uri('/api/users/'),
        'profiles': request.build_absolute_uri('/api/profiles/'),
        'activities': request.build_absolute_uri('/api/activities/'),
        'teams': request.build_absolute_uri('/api/teams/'),
        'leaderboards': request.build_absolute_uri('/api/leaderboards/'),
        'workouts': request.build_absolute_uri('/api/workouts/'),
    })

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', api_root, name='api-root'),
    path('api/', api_root, name='api-root'),
    path('api/', include(router.urls)),
    path('api-auth/', include('rest_framework.urls')),
]
