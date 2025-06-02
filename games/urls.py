from django.urls import path
from .views import *

urlpatterns = [    
    path('', login_view, name='login_page'), # GET for page, POST for login action via AJAX

    # Specific actions called by AJAX from the single login.html page
    path('signup/submit/', signup_view, name='signup_submit'), # POST for final user creation
    path('logout/', logout_view, name='logout'),
    
    path('send-verification-code/', send_verification_code_view, name='send_verification_code'),
    path('verify-email-code/', verify_email_code_view, name='verify_email_code'),
    
    path('check-auth-status/', check_auth_status_view, name='check_auth_status'),

    # Example other pages
    path('home/', home, name='home'), # Your home page
    path('game/', sudoku, name='sudoku_game'), # The main Sudoku game page
]
# Note: The above URLs are for the authentication system of Sudoku Arena.
# They handle login, signup, email verification, and logout functionality.