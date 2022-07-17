from django.urls import path
from . import views

urlpatterns = [
    path('home/', views.home, name='home'),
    path('signup/', views.signup, name='signup'),
    path('login/', views.login_view, name='login'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('lessons/', views.lessons, name='lessons'),
    path('<int:pk>', views.lesson, name="lesson"),
    path('importlesson/', views.importlesson, name='importlesson')
]