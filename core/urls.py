from django.urls import path
from .views import *

urlpatterns = [
      path('', index, name='index'),
      path('about/', about, name='about'),
      path('contact/', contact, name='contact'),
      path('pricing/', pricing, name='pricing'),
      path('blog/', blog, name='blog'),
]