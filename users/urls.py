from django.urls import path
from . import views

app_name = 'users'
urlpatterns = [
    path('', views.home.as_view(), name='home'),
    path('register/', views.registre.as_view(), name='register'),
    path('login/', views.login.as_view(), name='login'),
    path('dashboard/', views.dashboard.as_view(), name='dashboard'),
    path('logout/', views.logout.as_view(), name='logout'),
]