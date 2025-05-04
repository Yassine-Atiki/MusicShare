from django.urls import path
from . import views

app_name = 'users'
urlpatterns = [
    path('', views.home.as_view(), name='home'),
    path('register/', views.registre.as_view(), name='register'),
    path('login/', views.login.as_view(), name='login'),
    path('dashboard/', views.dashboard.as_view(), name='dashboard'),
    path('logout/', views.logout.as_view(), name='logout'),
    
    # Music related URLs
    path('upload/', views.upload_music.as_view(), name='upload_music'),
    path('track/<int:track_id>/', views.track_detail.as_view(), name='track_detail'),
    path('play/<int:track_id>/', views.play_track.as_view(), name='play_track'),
    
    # Playlist related URLs
    path('playlists/', views.playlists.as_view(), name='playlists'),
    path('playlist/create/', views.create_playlist.as_view(), name='create_playlist'),
    path('playlist/<int:playlist_id>/', views.playlist_detail.as_view(), name='playlist_detail'),
    path('playlist/<int:playlist_id>/add/<int:track_id>/', views.add_to_playlist.as_view(), name='add_to_playlist'),
    path('playlist/<int:playlist_id>/remove/<int:track_id>/', views.remove_from_playlist.as_view(), name='remove_from_playlist'),
    
    # User profile related URLs
    path('profile/', views.profile.as_view(), name='profile'),
    path('profile/edit/', views.edit_profile.as_view(), name='edit_profile'),
    path('profile/delete/', views.delete_account.as_view(), name='delete_account'),
    path('history/', views.history.as_view(), name='history'),
    path('history/clear/', views.clear_history.as_view(), name='clear_history'),

    # Playlist edit/delete URLs
    path('playlists/<int:playlist_id>/edit/', views.edit_playlist.as_view(), name='edit_playlist'),
    path('playlists/<int:playlist_id>/delete/', views.delete_playlist.as_view(), name='delete_playlist'),

    # API URLs
    path('api/user-tracks/', views.user_tracks.as_view(), name='user_tracks'),
]