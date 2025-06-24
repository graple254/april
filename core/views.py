from django.shortcuts import render, redirect
from .models import *


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