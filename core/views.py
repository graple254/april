from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib.auth import authenticate, login, logout
from .auth import *
from .models import*
import time
import re
import logging

logger = logging.getLogger(__name__)

def authenticate_user(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return JsonResponse({"status": True, "message": "Login successful!"})
        else:
            return JsonResponse({"status": False, "error": "Invalid credentials"})

    return render(request, "login.html")


def send_verification_code(request):
    if request.method == "POST":
        email = request.POST.get("email")
        if not email:
            return JsonResponse({"status": False, "error": "Email is required"})

        timestamp = request.session.get("email_verification_timestamp")
        if timestamp and (time.time() - timestamp) < 60:
            return JsonResponse({"status": False, "error": "Wait 60 seconds before requesting again"})

        code = generate_verification_code()
        request.session["email_verification_code"] = code
        request.session["email_verification_address"] = email
        request.session["email_verification_timestamp"] = time.time()

        if send_verification_email(email, code):
            return JsonResponse({"status": True, "message": "Code sent to your email!"})
        return JsonResponse({"status": False, "error": "Failed to send code."})

    return JsonResponse({"status": False, "error": "Invalid request"})


def verify_email_code(request):
    if request.method != "POST":
        return JsonResponse({"status": False, "error": "Invalid method."}, status=405)

    code_entered = request.POST.get("code")
    stored_code = request.session.get("email_verification_code")
    timestamp = request.session.get("email_verification_timestamp")
    email = request.session.get("email_verification_address")

    if not code_entered:
        return JsonResponse({"status": False, "error": "Please enter a code."})

    if not stored_code or not timestamp or not email:
        return JsonResponse({"status": False, "error": "No code found. Request again."})

    if time.time() - float(timestamp) > 600:
        request.session.flush()
        return JsonResponse({"status": False, "error": "Code expired. Request a new one."})

    if stored_code == code_entered:
        request.session["verified_email"] = email
        return JsonResponse({"status": True, "message": "Email verified!"})

    return JsonResponse({"status": False, "error": "Invalid code."})


def user_signup(request):
    if request.method == "POST":
        email = request.POST.get("email")

        if request.session.get("verified_email") != email:
            return JsonResponse({"status": False, "error": "Email not verified"})

        username = request.POST.get("username")
        password = request.POST.get("password")
        confirm_password = request.POST.get("confirm_password")

        if not all([username, email, password, confirm_password]):
            return JsonResponse({"status": False, "error": "All fields are required"})

        if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
            return JsonResponse({"status": False, "error": "Invalid email format"})

        response = register_user(username, email, password, confirm_password)

        if response["status"]:
            user = authenticate(request, username=username, password=password)
            if user:
                login(request, user)
            request.session.flush()
            return JsonResponse({"status": True, "message": "Signup successful!"})

        return JsonResponse({"status": False, "error": response["error"]})

    return JsonResponse({"status": False, "error": "Invalid request"})


def logout_user(request):
    logout(request)
    return redirect("index")

# END OF AUTHENTICATION VIEWS AND FUNCTIONALITIES #######################################################################

def index(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        content = request.POST.get('message')
        if email and content:
            Message.objects.create(email=email, content=content)
            return redirect('index')  # prevents form resubmission on refresh

    # Fetch content
    hero_info = hero.objects.last()
    platform_details = platform_detail.objects.all()
    contact_info = Contact.objects.first()
    social_media_info = social_media.objects.all()

    context = {
        'hero_info': hero_info,
        'platform_details': platform_details,
        'contact_info': contact_info,
        'social_media_info': social_media_info,
    }

    return render(request, 'index.html', context)


