from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.user_login, name='login'),
    path('signup/', views.user_signup, name='signup'),
    path('verify/', views.verify, name='verify'),
    path('verify-email/<uuid:token>/', views.verify_email, name='verify_email'),
    path('logout/', views.user_logout, name='logout'),
    path('', views.index, name='index'),
    path('home/', views.home, name='home'),
]