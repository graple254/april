from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User # If needed for direct queries, otherwise request.user is fine
from django.http import JsonResponse
from django.contrib import messages # Kept if you intend to use Django messages framework
import time
import re
from .auth import * # Assuming auth.py contains the necessary functions like register_user, send_successful_registration_email, etc.

# --- Authentication Views ---

def login_view(request):
    """Handles user login."""
    if request.user.is_authenticated:
        return redirect("home") 

    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        if not username or not password:
            return JsonResponse({"status": False, "error": "Username and password are required"}, status=400)

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return JsonResponse({"status": True, "message": "Login successful!", "redirect_url": "home"}) # Example redirect
        else:
            return JsonResponse({"status": False, "error": "Invalid username or password"}, status=401)

    return render(request, "files/login.html")




def logout_view(request):
    """Logs out the user and redirects."""
    logout(request)
    messages.success(request, "You have been successfully logged out.") # Example of using Django messages
    return redirect("login_page")  # Redirect to the login page after logout




def signup_view(request):
    """Handles user signup page display (GET) and form submission (POST for AJAX)."""
    if request.user.is_authenticated:
        return redirect("home")

    if request.method == "POST": 
        email = request.POST.get("email")
        
        if request.session.get("verified_email") != email:
            return JsonResponse({"status": False, "error": "Email not verified or session mismatch."}, status=403)

        username = request.POST.get("username")
        password = request.POST.get("password")
        confirm_password = request.POST.get("confirm_password")

        if not all([username, email, password, confirm_password]):
            return JsonResponse({"status": False, "error": "All fields (username, email, password, confirm) are required"}, status=400)

        if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
            return JsonResponse({"status": False, "error": "Invalid email format"}, status=400)
        
        response = register_user(username, email, password, confirm_password)
        
        if response["status"]:
            user = authenticate(request, username=username, password=password)
            if user:
                login(request, user)
            
            send_successful_registration_email(email, username)

            for key in ["verified_email", "email_verification_code", "email_verification_timestamp", "email_verification_address"]:
                if key in request.session:
                    del request.session[key]
            
            return JsonResponse({"status": True, "message": "User registered successfully! Welcome!", "redirect_url": "home"})
        else:
            return JsonResponse({"status": False, "error": response.get("error", "Registration failed.")}, status=400)

    return JsonResponse({"status": False, "error": "Invalid request method."}, status=405) # For non-POST requests




def send_verification_code_view(request):
    """Sends an email verification code to the user's email via AJAX POST."""
    if request.method == "POST":
        email = request.POST.get("email")

        if not email:
            return JsonResponse({"status": False, "error": "Email is required"}, status=400)
        
        if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
            return JsonResponse({"status": False, "error": "Invalid email format"}, status=400)

        timestamp = request.session.get("email_verification_timestamp")
        if timestamp and (time.time() - timestamp) < 60: 
            return JsonResponse({"status": False, "error": "Please wait 60 seconds before requesting a new code."}, status=429)

        code = generate_verification_code()
        request.session["email_verification_code"] = code
        request.session["email_verification_address"] = email
        request.session["email_verification_timestamp"] = time.time() 
        request.session.set_expiry(600) 

        if send_verification_email(email, code):
            return JsonResponse({"status": True, "message": "Verification code sent to your email!"})
        else:
            return JsonResponse({"status": False, "error": "Failed to send verification code. Please try again later."}, status=500)

    return JsonResponse({"status": False, "error": "Invalid request method."}, status=405)



# your_sudoku_app/views.py

# ... (other imports) ...
# from .auth import generate_verification_code, send_verification_email, send_successful_registration_email, register_user # Ensure this is correct

def verify_email_code_view(request):
    """Verifies the email code entered by the user against the stored code via AJAX POST."""
    if request.method != "POST":
        return JsonResponse({"status": False, "error": "Invalid request method."}, status=405)

    code_entered = request.POST.get("code")
    
    # Get current verification attempt details from session
    stored_code = request.session.get("email_verification_code")
    timestamp = request.session.get("email_verification_timestamp") 
    current_email_being_verified = request.session.get("email_verification_address") # Email for *this specific code*
    
    # For debugging, print what's in session at the start of this view
    # print(f"[VerifyView] Session at start: code={stored_code}, ts={timestamp}, addr={current_email_being_verified}, verified_email={request.session.get('verified_email')}")


    if not code_entered:
        return JsonResponse({"status": False, "error": "Please enter a verification code."}, status=400)

    # This checks if a verification process (sending a code) was actually initiated for current_email_being_verified
    if not stored_code or not timestamp or not current_email_being_verified:
        # If these are missing, it means either no code was sent, or it expired and was cleared,
        # or a previous verification for a *different* email cleared them.
        # We should not proceed with verification.
        # Also, clear any potentially stale "verified_email" if the current attempt is failing this early.
        # This prevents a jump to signup if a previous unrelated email was verified.
        # However, be careful: if a user legitimately verified email_A, then tries to verify email_B but fails
        # at this stage, should email_A's "verified_email" status be revoked?
        # For now, let's assume if they are at "enter code" step, they are trying to verify current_email_being_verified.
        # If that process is broken, then the "verified_email" from a *previous* successful flow for a *different* email
        # shouldn't allow them to skip to signup with the *current failing* email.
        
        # Let's clear all verification-specific keys to force a restart of the process
        for key in ["email_verification_code", "email_verification_address", "email_verification_timestamp", "verified_email"]:
            request.session.pop(key, None)
        return JsonResponse({"status": False, "error": "Verification process invalid or expired. Please request a new code."}, status=400)

    if time.time() - timestamp > 600: # 10 minutes expiry
        for key in ["email_verification_code", "email_verification_address", "email_verification_timestamp"]:
            request.session.pop(key, None)
        # Also clear verified_email if the code for *it* expired.
        if request.session.get("verified_email") == current_email_being_verified:
            request.session.pop("verified_email", None)
        return JsonResponse({"status": False, "error": "Verification code has expired. Please request a new one."}, status=400)

    if stored_code == code_entered:
        # Code is correct for current_email_being_verified
        request.session["verified_email"] = current_email_being_verified # This is the email that is now confirmed
        
        # Clear the session keys related to *this specific verification attempt*
        request.session.pop("email_verification_code", None)
        request.session.pop("email_verification_timestamp", None)
        request.session.pop("email_verification_address", None) # Clear this too, as this attempt is done.
                                                              # "verified_email" now holds the successfully verified one.
        
        # print(f"[VerifyView] Code OK. Session after success: verified_email={request.session.get('verified_email')}")
        return JsonResponse({"status": True, "message": "Email verified successfully!"})
    else:
        # Incorrect code. Don't change "verified_email" if it was set from a previous, different, successful verification.
        # Just report error for the current attempt.
        # print(f"[VerifyView] Code BAD. Session state unchanged for verified_email.")
        return JsonResponse({"status": False, "error": "Invalid verification code."}, status=400)

# ... rest of your views.py ...



def check_auth_status_view(request):
    """Simplified check for user authentication status."""
    data = {
        "is_authenticated": request.user.is_authenticated,
        "username": request.user.username if request.user.is_authenticated else None,
    }
    return JsonResponse(data)



def sudoku(request):
    return render(request, 'files/sudoku.html')


def home(request):
    """Render the home page."""
    return render(request, 'files/home.html')


# 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