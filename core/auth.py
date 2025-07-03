from django.contrib.auth import authenticate, login
from django.contrib.auth.hashers import make_password
from .models import User
import random
import logging
import sib_api_v3_sdk
from sib_api_v3_sdk.rest import ApiException

def generate_verification_code():
    """Generate a 6-digit random verification code."""
    return str(random.randint(100000, 999999))

logger = logging.getLogger(__name__)

def send_verification_email(email, code):
    """Send a verification code using Brevo API."""
    api_key = (
        "xkeysib"
        "-65f87098e4405520b41fc9ac188abfbabd646ea947a9045a9ccde4c94795bdc8"
        "-5NIDZuBUzrO0j1XU"
    )

    configuration = sib_api_v3_sdk.Configuration()
    configuration.api_key['api-key'] = api_key

    api_instance = sib_api_v3_sdk.TransactionalEmailsApi(
        sib_api_v3_sdk.ApiClient(configuration)
    )

    subject = "Your Email Verification Code"
    html_content = f"""
    <html>
        <body>
            <p>Hello,</p>
            <p>Your verification code is:</p>
            <h2>{code}</h2>
            <p>Use it to complete your signup on Jadoo 📚</p>
        </body>
    </html>
    """

    sender = {"email": "victorokoth@jadoo.world", "name": "Jadoo"}
    to = [{"email": email}]
    send_smtp_email = sib_api_v3_sdk.SendSmtpEmail(
        to=to,
        html_content=html_content,
        subject=subject,
        sender=sender
    )

    try:
        api_instance.send_transac_email(send_smtp_email)
        logger.info(f"Verification email sent to {email}")
        return True
    except ApiException as e:
        logger.error(f"Failed to send verification email: {str(e)}")
        return False


def register_user(username, email, password, confirm_password):
    """Registers a new user with basic fields only."""
    if password != confirm_password:
        return {"status": False, "error": "Passwords do not match"}

    if User.objects.filter(username=username).exists():
        return {"status": False, "error": "Username already exists"}

    if User.objects.filter(email=email).exists():
        return {"status": False, "error": "Email already in use"}

    user = User.objects.create(
        username=username,
        email=email,
        password=make_password(password)
    )

    return {"status": True, "user": user.username}


def authenticate_user_func(request, username, password):
    """Handles user authentication and logs them in if valid."""
    if not username or not password:
        return {"status": False, "error": "Username and password are required"}

    user = authenticate(request, username=username, password=password)

    if user:
        login(request, user)
        return {"status": True, "user": user.username}
    else:
        return {"status": False, "error": "Invalid credentials"}

