# core/auth.py (or your_sudoku_app/auth_utils.py)

from django.contrib.auth import authenticate, login
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User # Using Django's default User model
import random
from django.conf import settings
import sib_api_v3_sdk
from sib_api_v3_sdk.rest import ApiException

def generate_verification_code():
    """Generate a 6-digit random verification code."""
    return str(random.randint(100000, 999999))

def _send_email_brevo(recipient_email, subject, html_content, sender_display_name="Jadoo Team"):
    """
    Helper function to send email using Brevo (Sendinblue).
    recipient_email: The email address of the person receiving the email.
    subject: The subject of the email.
    html_content: The HTML content of the email.
    sender_display_name: The "From" name displayed to the recipient.
    """
    
    # 1. API Key Configuration (Keep this secure)
    # Consider using environment variables for your API key in production.
    # The split key method is basic obfuscation.
    part1 = "xkeysib"  # Replace with your actual key parts or use settings.BREVO_API_KEY
    part2 = "-1a242f7c72a5da47d738050341dea3976f5f2af9316672d719e8d13f7b0124f9" 
    part3 = "-jJf3Zgcj78y2h9mC" # Example key parts
    api_key_brevo = part1 + part2 + part3  # Final key

    configuration = sib_api_v3_sdk.Configuration()
    configuration.api_key['api-key'] = api_key_brevo

    api_instance = sib_api_v3_sdk.TransactionalEmailsApi(
        sib_api_v3_sdk.ApiClient(configuration)
    )

    # 2. Sender Email Configuration (CRUCIAL)
    # This email address MUST be a sender you have verified in your Brevo account.
    # It's best to configure this in your Django settings.py file.
    # Example: In settings.py -> SUDOKU_ARENA_SENDER_EMAIL = 'your_verified_email@yourdomain.com'
    
    actual_sender_email = 'chargeke@gmail.com'

    if not actual_sender_email:
        print("CRITICAL WARNING: settings.SUDOKU_ARENA_SENDER_EMAIL is not configured in your Django settings.py!")
        print("Email sending will likely fail. Please set it to your Brevo verified sender email address.")
        # Fallback to a placeholder that will cause an error if not changed, to highlight the misconfiguration.
        # You MUST replace this with your actual verified sender or configure it in settings.py
        actual_sender_email = 'chargeke@gmail.com' 
    
    sender_info = {"email": actual_sender_email, "name": sender_display_name}
    to = [{"email": recipient_email}]
    
    send_smtp_email = sib_api_v3_sdk.SendSmtpEmail(
        to=to,
        html_content=html_content,
        subject=subject,
        sender=sender_info
    )

    try:
        api_instance.send_transac_email(send_smtp_email)
        # For development, you might want to print a success message here
        # print(f"Email sent successfully to {recipient_email} from {actual_sender_email} with subject: {subject}")
        return True
    except ApiException as e:
        # Print the full error for debugging
        print(f"Failed to send email to {recipient_email} from {actual_sender_email}. Brevo API Error: {e}")
        return False

def send_verification_email(email, code):
    """Send a verification code email for Sudoku Arena."""
    subject = "Your Jadoo Email Verification Code"
    html_content = f"""
    <html>
        <body>
            <p>Hello,</p>
            <p>Your verification code for Jadoo is:</p>
            <h2>{code}</h2>
            <p>Use this code to complete your registration.</p>
            <p>If you didn't request this, please ignore this email.</p>
            <p>Thanks,<br>The Jadoo Team</p>
        </body>
    </html>
    """
    # The sender_display_name here is "Sudoku Arena Team"
    return _send_email_brevo(email, subject, html_content, sender_display_name="Jadoo Team")

def send_successful_registration_email(email, username):
    """Send a welcome email after successful registration for Sudoku Arena."""
    subject = "Welcome to Jadoo!"
    html_content = f"""
    <html>
        <body>
            <p>Hello {username},</p>
            <p>Welcome to Jadoo! Your registration was successful.</p>
            <p>You can now log in and start playing. We hope you enjoy the challenge!</p>
            <p>Happy puzzling!</p>
            <p>Thanks,<br>The Jadoo Team</p>
        </body>
    </html>
    """
    # The sender_display_name here is also "Sudoku Arena Team"
    return _send_email_brevo(email, subject, html_content, sender_display_name="Jadoo Team")

def register_user(username, email, password, confirm_password):
    """Handles user registration for Jadoo."""
    if password != confirm_password:
        return {"status": False, "error": "Passwords do not match"}

    if User.objects.filter(username=username).exists():
        return {"status": False, "error": "Username already exists"}

    if User.objects.filter(email=email).exists():
        return {"status": False, "error": "Email already in use"}

    try:
        user = User.objects.create_user( 
            username=username,
            email=email,
            password=password 
        )
        return {"status": True, "user_id": user.id, "username": user.username}
    except Exception as e:
        # print(f"Error creating user {username} ({email}): {str(e)}") # Optional for dev
        return {"status": False, "error": "An error occurred during registration. Please try again."}