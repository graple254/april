from django.db import models
from django.utils import timezone


class Profile(models.Model):
    image = models.ImageField(upload_to='profile_images', blank=True, null=True)

    def __str__(self):
        return f"Profile Image: {self.image.url if self.image else 'No image uploaded'}"

class Visitor(models.Model):
    ip_address = models.GenericIPAddressField(blank=True, null=True)
    location = models.CharField(max_length=255, blank=True, null=True)
    user_agent = models.TextField(blank=True, null=True)
    url_path = models.CharField(max_length=500, blank=True, null=True)
    method = models.CharField(max_length=10, blank=True, null=True)
    referrer = models.URLField(blank=True, null=True)
    visit_date = models.DateTimeField(default=timezone.now, blank=True, null=True)

    def __str__(self):
        return f"{self.ip_address} visited {self.url_path} on {self.visit_date}"

   

class Contact(models.Model): 
    whatsapp_number = models.CharField(max_length=20, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)

    def __str__(self):
        return f"Contact: {self.whatsapp_number}, {self.email}"


class hero(models.Model):
    title = models.CharField(max_length=255, blank=True, null=True)
    subtitle = models.TextField(blank=True, null=True)
    launch_date = models.DateField(blank=True, null=True)

    def __str__(self):
        return f"Hero: {self.title} - {self.subtitle}" 
    


class platform_detail(models.Model):
    attached = models.ForeignKey(hero, on_delete=models.CASCADE, blank=True, null=True)
    title = models.CharField(max_length=255, blank=True, null=True)
    subtitle = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Platform: {self.title} - {self.subtitle}"
    
    

class detail(models.Model):
    attached = models.ForeignKey(platform_detail, on_delete=models.CASCADE, blank=True, null=True)
    title = models.CharField(max_length=255, blank=True, null=True)
    subtitle = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Detail: {self.title} - {self.subtitle}"
    

class social_media(models.Model):
    twitter = models.URLField(blank=True, null=True)
    facebook = models.URLField(blank=True, null=True)
    instagram = models.URLField(blank=True, null=True)
    youtube = models.URLField(blank=True, null=True)
    tiktok = models.URLField(blank=True, null=True)
    linkedin = models.URLField(blank=True, null=True)

    def __str__(self):
        return f"Social Media: {self.twitter}, {self.tiktok}, {self.linkedin}"
