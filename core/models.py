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


class SEOMetaTag(models.Model):
    # Standard Meta Tags
    description = models.TextField(blank=True, null=True)
    author = models.CharField(max_length=255, blank=True, null=True)
    keywords = models.TextField(blank=True, null=True)
    robots = models.CharField(
        max_length=255, 
        default="index, follow, max-image-preview:large, max-snippet:-1, max-video-preview:-1",
        blank=True, null=True
    )

    # Dublin Core Tags
    dc_title = models.CharField(max_length=255, blank=True, null=True)
    dc_description = models.TextField(blank=True, null=True)
    dc_creator = models.CharField(max_length=255, blank=True, null=True)
    dc_publisher = models.CharField(max_length=255, blank=True, null=True)
    dc_subject = models.TextField(blank=True, null=True)
    dc_type = models.CharField(max_length=100, default="website", blank=True, null=True)
    dc_format = models.CharField(max_length=100, default="text/html", blank=True, null=True)
    dc_language = models.CharField(max_length=20, default="en-US", blank=True, null=True)
    dc_rights = models.CharField(
        max_length=255,
        default=f"Copyright © {timezone.now().year} Jadoo. All rights reserved.", blank=True, null=True
    )

    updated_at = models.DateTimeField(auto_now=True, blank=True, null=True)

    def __str__(self):
        return f"SEO Metadata - Last updated on {self.updated_at.strftime('%Y-%m-%d')}"

    class Meta:
        verbose_name = "SEO Meta Tag"
        verbose_name_plural = "SEO Meta Tags"


# Index.html dynamic models here ----------------------------------------------------------------------

class HeroSection(models.Model):
    main_title_1 = models.TextField(blank=True, null=True)  # Supports line breaks (e.g., "Ads don't sell")
    main_title_2 = models.TextField(blank=True, null=True)  # Supports line breaks (e.g., "People do")
    highlighted_title = models.CharField(max_length=200, blank=True, null=True) # Unleash human .....

    text_1 = models.TextField(blank=True, null=True)  # Supports line breaks (e.g., "Your ads are getting ignored")
    text_2 = models.TextField(blank=True, null=True)  # Supports line breaks (e.g., "so ditch them")
    text_3 = models.TextField(blank=True, null=True)  # Supports line breaks (e.g., "so skip them")
    text_4 = models.TextField(blank=True, null=True)  # Supports line breaks (e.g., "Tap into real influence")


    affirmative_text = models.TextField(blank=True, null=True) #Jadoo activates ......

    def __str__(self):
        return "Hero Section"
    
class Why_jadoo(models.Model):
    text_title_1 = models.TextField(blank=True, null=True)  # why
    text_title_2 = models.TextField(blank=True, null=True)  # Jadoo
    text_title_3 = models.TextField(blank=True, null=True)  # Matters
    text_title_4 = models.TextField(blank=True, null=True)  # Built for brands
    text_title_5 = models.TextField(blank=True, null=True)  # Now

    paragraph = models.TextField(blank=True, null=True)  # Consumers skip ads....

    def __str__(self):
        return "Why Jadoo Section"
    

class How_it_works(models.Model):
    text_title_1 = models.TextField(blank=True, null=True)  # How 
    text_title_2 = models.TextField(blank=True, null=True)  # Jadoo
    text_title_3 = models.TextField(blank=True, null=True)  # Works
    subtitle_text = models.TextField(blank=True, null=True)  # Connecting brands ..

    title_1 = models.TextField(blank=True, null=True)
    title_1_text = models.TextField(blank=True, null=True)

    title_2 = models.TextField(blank=True, null=True)
    title_2_text = models.TextField(blank=True, null=True)

    title_3 = models.TextField(blank=True, null=True)
    title_3_text = models.TextField(blank=True, null=True)

    title_4 = models.TextField(blank=True, null=True)
    title_4_text = models.TextField(blank=True, null=True)

    def __str__(self):
        return "How it works Section"
    


class business_proposition(models.Model):
    text_title_1 = models.TextField(blank=True, null=True)  # Business
    text_title_2 = models.TextField(blank=True, null=True)  # Proposition

    def __str__(self):
        return "Business Proposition Section"
    

class business_proposition_modal(models.Model):
    text_title_1 = models.TextField(blank=True, null=True)  # Business
    text_title_2 = models.TextField(blank=True, null=True)  # Proposition

    card_title_1 = models.TextField(blank=True, null=True)  # Name of plan
    basic_price = models.CharField(max_length=20, blank=True, null=True)  # Basic plan price
    promise_1 = models.TextField(blank=True, null=True)  # Promise 1
    promise_2 = models.TextField(blank=True, null=True)  # Promise 2
    promise_3 = models.TextField(blank=True, null=True)  # Promise 3

    notification_text = models.TextField(blank=True, null=True)  # Notification text

    def __str__(self):
        return "Business Proposition Modal Section"

    

class Brands_we_work_with(models.Model):
    text_title_1 = models.TextField(blank=True, null=True)  # Brands
    text_title_2 = models.TextField(blank=True, null=True)  # We work with


    def __str__(self):
        return "Brands we work with Section"
    

class Brands(models.Model):
    brands = models.ForeignKey(Brands_we_work_with, on_delete=models.CASCADE, blank=True, null=True)  # Foreign key to Brands_we_work_with
    brand_name = models.CharField(max_length=200, blank=True, null=True)  # Brand name
    brand_bi_bi = models.TextField(blank=True, null=True)  # Brand bio or description

    def __str__(self):
        return self.brand_name
    

class cretor_proposition(models.Model):
    text_title_1 = models.TextField(blank=True, null=True)  # Creators
    text_title_2 = models.TextField(blank=True, null=True)  # Invitation

    def __str__(self):
        return "Creator Invitation Card Section"
    


class creator_proposition_modal(models.Model):
    text_title_1 = models.TextField(blank=True, null=True)  # Creators
    text_title_2 = models.TextField(blank=True, null=True)  # Invitation

    card_title_1 = models.TextField(blank=True, null=True)  # Name of plan
    promise_1 = models.TextField(blank=True, null=True)  # Promise 1
    promise_2 = models.TextField(blank=True, null=True)  # Promise 2

    card_title_2 = models.TextField(blank=True, null=True)  # Name of plan
    promise_3 = models.TextField(blank=True, null=True)  # Promise 3

    card_title_3 = models.TextField(blank=True, null=True)  # Name of plan
    promise_4 = models.TextField(blank=True, null=True)  # Promise 4

    card_title_4 = models.TextField(blank=True, null=True)  # Name of plan
    promise_5 = models.TextField(blank=True, null=True)  # Promise 5
    promise_6 = models.TextField(blank=True, null=True)  # Promise 6

    notification_text = models.TextField(blank=True, null=True)  # Notification text

    def __str__(self):
        return "Creator Proposition Modal Section"
    
    

class Privacy_policy(models.Model):
    text_title_1 = models.TextField(blank=True, null=True)  
    text_1 = models.TextField(blank=True, null=True) 

    text_title_2 = models.TextField(blank=True, null=True)
    text_2 = models.TextField(blank=True, null=True)

    text_title_3 = models.TextField(blank=True, null=True)
    text_3 = models.TextField(blank=True, null=True)

    text_title_4 = models.TextField(blank=True, null=True)
    text_4 = models.TextField(blank=True, null=True)

    def __str__(self):
        return "Privacy Policy Section"   

class Terms_and_conditions(models.Model):  
    text_title_1 = models.TextField(blank=True, null=True)  
    text_1 = models.TextField(blank=True, null=True) 

    text_title_2 = models.TextField(blank=True, null=True)
    text_2 = models.TextField(blank=True, null=True)

    text_title_3 = models.TextField(blank=True, null=True)
    text_3 = models.TextField(blank=True, null=True)

    text_title_4 = models.TextField(blank=True, null=True)
    text_4 = models.TextField(blank=True, null=True)

    def __str__(self):
        return "Terms and Conditions Section"   
    

class refund_policy(models.Model):
    text_title_1 = models.TextField(blank=True, null=True)  
    text_1 = models.TextField(blank=True, null=True) 

    text_title_2 = models.TextField(blank=True, null=True)
    text_2 = models.TextField(blank=True, null=True)

    text_title_3 = models.TextField(blank=True, null=True)
    text_3 = models.TextField(blank=True, null=True)

    text_title_4 = models.TextField(blank=True, null=True)
    text_4 = models.TextField(blank=True, null=True)

    def __str__(self):
        return "Refund Policy Section"      


class Contact_us(models.Model):
    whatsapp_number = models.CharField(max_length=20, blank=True, null=True)  # WhatsApp number
    email = models.EmailField(blank=True, null=True)  # Email address

    def __str__(self):
        return "Contact Us Section"
    

class Blog(models.Model):
    title_1 = models.TextField(blank=True, null=True)  # Blog
    summary_text = models.TextField(blank=True, null=True)  # Jadoo
    full_text = models.TextField(blank=True, null=True)  # Matters

    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)  # Date and time of creation

    def __str__(self):
        return "Blog Section"    
    
    