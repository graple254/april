from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import *


def index(request):
      return render(request, 'landing/index.html')

def about(request):
      return render(request, 'landing/about.html')

def contact(request):
      return render(request, 'landing/contact.html')

def pricing(request):
      return render(request, 'landing/pricing.html')

def blog(request):
      return render(request, 'landing/blog.html')

