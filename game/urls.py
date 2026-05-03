from django.urls import path
from . import views

urlpatterns = [
    path('', views.login_view, name='root'),
    path('home/', views.home, name='home'),

    path('missions/', views.missions_view, name='missions'),
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),

    path('submit-proof/<int:mission_id>/', views.submit_proof, name='submit_proof'),

    path('leaderboard/', views.leaderboard_view, name='leaderboard'),
    path('profile/', views.profile_view, name='profile'),

    path('chat/', views.chat_view, name='chat'),
    path('chat-api/', views.chat_api, name='chat_api'),
]