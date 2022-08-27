from django.urls import path
from . import views

urlpatterns = [
    path('home/', views.home, name='home'),
    # path('signup/', views.signup_view, name='signup_view'),
    # path('login/', views.login_view, name='login_view'),
    # path('dashboard/', views.dashboard, name='dashboard'),
    path('lessons/', views.lessons, name='lessons'),
    path('change_translation/', views.change_translation, name='change_translation'),
    path('<int:pk>', views.lesson, name="lesson"),
    path('importlesson/', views.importlesson, name='importlesson')
]