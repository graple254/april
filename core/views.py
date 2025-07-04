from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User
from django.views.decorators.csrf import ensure_csrf_cookie
from django.utils import timezone
from django.db.models import Q
from .models import *
import sib_api_v3_sdk
from sib_api_v3_sdk.rest import ApiException
import logging
import re

logger = logging.getLogger(__name__)

######################################################################################################
def send_verification_email(request, user, token):
    """Send a verification email with a unique link using Brevo API."""
    a1 = "xkeysib"
    a2 = "-65f87098e4405520b41fc9ac188abfbabd646ea947a9045a9ccde4c94795bdc8"
    a3 = "-5NIDZuBUzrO0j1XU"
    api_key = a1 + a2 + a3
    configuration = sib_api_v3_sdk.Configuration()
    configuration.api_key["api-key"] = api_key
    api_instance = sib_api_v3_sdk.TransactionalEmailsApi(sib_api_v3_sdk.ApiClient(configuration))

    verification_url = f"{request.scheme}://{request.get_host()}/verify-email/{token.token}/"
    subject = "Verify Your Jadoo Account"
    html_content = f"""
    <html>
        <body>
            <h2>Welcome to Jadoo!</h2>
            <p>Hi {user.username},</p>
            <p>Please verify your email by clicking the link below:</p>
            <a href="{verification_url}" style="display: inline-block; padding: 10px 20px; background-color: #000000; color: #ffffff; text-decoration: none; border-radius: 5px;">Verify Email</a>
            <p>This link will expire in 24 hours.</p>
            <p>If you didn’t sign up for Jadoo, please ignore this email.</p>
            <p>Happy studying! 📚</p>
            <p>The Jadoo Team</p>
        </body>
    </html>
    """

    sender = {"email": "victorokoth@jadoo.world", "name": "Jadoo"}
    to = [{"email": user.email}]
    send_smtp_email = sib_api_v3_sdk.SendSmtpEmail(
        to=to, html_content=html_content, subject=subject, sender=sender
    )

    try:
        api_instance.send_transac_email(send_smtp_email)
        logger.info(f"Verification email sent to {user.email} with token {token.token}")
        return True
    except ApiException as e:
        logger.error(f"Failed to send verification email to {user.email}: {str(e)}")
        return False

@ensure_csrf_cookie
def user_login(request):
    """Handle user login and render login page."""
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        
        if not username or not password:
            logger.warning("Login attempt with missing credentials")
            return JsonResponse({"status": False, "error": "Username and password are required"})

        user = authenticate(request, username=username, password=password)
        if user:
            if user.is_active:
                login(request, user)
                logger.info(f"User {username} logged in successfully")
                return JsonResponse({"status": True, "message": "Login successful!"})
            else:
                logger.warning(f"Login attempt by unverified user: {username}")
                return JsonResponse({"status": False, "error": "Please verify your email first"})
        else:
            logger.warning(f"Invalid login attempt for username: {username}")
            return JsonResponse({"status": False, "error": "Invalid credentials"})

    return render(request, "login.html")

@ensure_csrf_cookie
def user_signup(request):
    """Handle user signup, create unverified user, and redirect to verify page."""
    if request.method == "POST":
        email = request.POST.get("email")
        username = request.POST.get("username")
        password = request.POST.get("password")
        confirm_password = request.POST.get("confirm_password")

        if not all([email, username, password, confirm_password]):
            logger.warning("Signup attempt with missing fields")
            return JsonResponse({"status": False, "error": "All fields are required"})

        if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
            logger.warning(f"Invalid email format: {email}")
            return JsonResponse({"status": False, "error": "Invalid email format"})

        if password != confirm_password:
            logger.warning(f"Password mismatch for user: {username}")
            return JsonResponse({"status": False, "error": "Passwords do not match"})

        if User.objects.filter(username=username).exists():
            logger.warning(f"Username already exists: {username}")
            return JsonResponse({"status": False, "error": "Username already exists"})

        if User.objects.filter(email=email).exists():
            logger.warning(f"Email already in use: {email}")
            return JsonResponse({"status": False, "error": "Email already in use"})

        try:
            user = User.objects.create(
                username=username,
                email=email,
                password=make_password(password),
                is_active=False
            )
            token = EmailVerificationToken.objects.create(user=user)
            if send_verification_email(request, user, token):
                logger.info(f"User {username} created, verification email sent")
                request.session["pending_email"] = email  # Store email for verify page
                return JsonResponse({"status": True, "redirect": "/verify/"})
            else:
                user.delete()  # Rollback if email fails
                logger.error(f"Failed to send verification email for {username}")
                return JsonResponse({"status": False, "error": "Failed to send verification email"})
        except Exception as e:
            logger.error(f"Error during signup for {username}: {str(e)}")
            return JsonResponse({"status": False, "error": "An error occurred during signup"})

    return render(request, "signup.html")

@ensure_csrf_cookie
def verify(request):
    """Render verify page to instruct user to check email."""
    email = request.session.get("pending_email")
    if not email:
        logger.warning("Access to verify page without pending email")
        return render(request, "verify.html", {"error": "No pending verification. Please sign up first."})
    return render(request, "verify.html", {"email": email})

def verify_email(request, token):
    """Verify user email using token and redirect to index."""
    try:
        token_obj = EmailVerificationToken.objects.get(token=token)
        if token_obj.is_valid():
            user = token_obj.user
            user.is_active = True
            user.save()
            token_obj.is_used = True
            token_obj.save()
            login(request, user)
            request.session.pop("pending_email", None)  # Clear session
            logger.info(f"User {user.username} verified and logged in")
            return redirect("home")  # Redirect to home page after verification
        else:
            logger.warning(f"Invalid or expired token: {token}")
            return render(request, "verify.html", {"error": "Invalid or expired verification link. Please sign up again."})
    except EmailVerificationToken.DoesNotExist:
        logger.warning(f"Token not found: {token}")
        return render(request, "verify.html", {"error": "Invalid verification link. Please sign up again."})

@ensure_csrf_cookie
def user_logout(request):
    """Log out the user and redirect to login page."""
    if request.method == "POST":
        logout(request)
        logger.info("User logged out successfully")
        return JsonResponse({"status": True, "message": "Logged out successfully"})
    return redirect("login")

###############################################################################################################

def home(request):
    """Render the index page after successful login or verification."""
    if not request.user.is_authenticated:
        logger.warning("Unauthorized access attempt to index page")
        return redirect("login")

    return render(request, "home.html")

@ensure_csrf_cookie
def index(request):

    if request.method == "POST":
        email = request.POST.get("email")
        content = request.POST.get("message")
        if email and content:
            Message.objects.create(email=email, content=content)
            logger.info(f"Contact message saved from {email}")
            return redirect("index")  # Prevents form resubmission

    hero_info = hero.objects.last()
    platform_details = platform_detail.objects.all()
    contact_info = Contact.objects.first()
    social_media_info = social_media.objects.all()

    context = {
        "hero_info": hero_info,
        "platform_details": platform_details,
        "contact_info": contact_info,
        "social_media_info": social_media_info,
        "username": request.user.username,
    }

    return render(request, "index.html", context)



