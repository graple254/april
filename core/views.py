from django.shortcuts import render
from .models import *

def index(request):
    # Fetch the latest hero, platform details, and contact information
    hero_info = hero.objects.last()  # Get the latest Hero object
    platform_details = platform_detail.objects.all()  # Get all Platform details
    contact_info = Contact.objects.first()  # Get the first Contact object (assuming you only have one)
    social_media_info = social_media.objects.all()  # Get all Social Media objects

    context = {
        'hero_info': hero_info,
        'platform_details': platform_details,
        'contact_info': contact_info,
        'social_media_info': social_media_info,
    }
    
    return render(request, 'index.html', context)