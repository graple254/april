from django.urls import path
from .views import *

urlpatterns = [
    path('index/', index, name='index'),  # Home page
    path('', authenticate_user, name='login'),  # Log in
    path('signup/', user_signup, name='signup'),  # Sign up
    path('send-verification-code/', send_verification_code, name='send_verification_code'),
    path('verify-email-code/', verify_email_code, name='verify_email_code'),
    path('logout/', logout_user, name='logout'),
]
