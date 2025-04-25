from django.db import models


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


    sub_title_1 = models.TextField(blank=True, null=True)  # create a campaign
    sb1_text_1 = models.TextField(blank=True, null=True)  # Choose a campaign type and set your budget
    sb1_text_2 = models.TextField(blank=True, null=True)  # Choose a campaign type and set your budget

    listing_1 = models.TextField(blank=True, null=True)  # Choose a campaign type and set your budget
    listing_1_text = models.TextField(blank=True, null=True)  # Choose a campaign type and set your budget

    listing_2 = models.TextField(blank=True, null=True)  # Choose a campaign type and set your budget
    listing_2_text = models.TextField(blank=True, null=True)  # Choose a campaign type and set your budget


    sub_title_2 = models.TextField(blank=True, null=True)  # Set a budget
    sb2_text_1 = models.TextField(blank=True, null=True)  # Choose a campaign type and set your budget
    sb2_text_2 = models.TextField(blank=True, null=True)  # Choose a campaign type and set your budget
    sb2_text_3 = models.TextField(blank=True, null=True)  # Choose a campaign type and set your budget

    detail_text_1 = models.TextField(blank=True, null=True)  # Choose a campaign type and set your budget

    dt_1 = models.TextField(blank=True, null=True)  # Choose a campaign type and set your budget
    dt_1_text = models.TextField(blank=True, null=True)  # Choose a campaign type and set your budget

    dt_2 = models.TextField(blank=True, null=True)  # Choose a campaign type and set your budget
    dt_2_text = models.TextField(blank=True, null=True)  # Choose a campaign type and set your budget

    dt_3 = models.TextField(blank=True, null=True)  # Choose a campaign type and set your budget
    dt_3_text = models.TextField(blank=True, null=True)  # Choose a campaign type and set your budget

    closing_text = models.TextField(blank=True, null=True)  # Choose a campaign type and set your budget


    sub_title_3 = models.TextField(blank=True, null=True)  # Reach the right Creators
    sb3_text_1 = models.TextField(blank=True, null=True)  # Choose a campaign type and set your budget


    sub_title_4 = models.TextField(blank=True, null=True)  # Choose a campaign type and set your budget
    sb4_text_1 = models.TextField(blank=True, null=True)  # Choose a campaign type and set your budget

    def __str__(self):
        return "How it works Section"
    

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
    

class cretor_invitation_card(models.Model):
    text_title_1 = models.TextField(blank=True, null=True)  # Creators
    text_title_2 = models.TextField(blank=True, null=True)  # Invitation

    def __str__(self):
        return "Creator Invitation Card Section"
    

class Privacy_policy(models.Model):
    text_title_1 = models.TextField(blank=True, null=True)  # Privacy
    text = models.TextField(blank=True, null=True)  # Policy

    def __str__(self):
        return "Privacy Policy Section"   

class Terms_and_conditions(models.Model):  
    text_title_1 = models.TextField(blank=True, null=True)  # Terms
    text = models.TextField(blank=True, null=True)  # And

    def __str__(self):
        return "Terms and Conditions Section"   
    


# End of Index.html dynamic models here ----------------------------------------------------------------------
# 
#     


# Start of About.html dynamic models here ----------------------------------------------------------------------



# End of About.html dynamic models here ----------------------------------------------------------------------
#
#


# Start of Contact.html dynamic models here ----------------------------------------------------------------------



# End of Contact.html dynamic models here ----------------------------------------------------------------------
#
#


# Start of pricing.html dynamic models here ----------------------------------------------------------------------




#End of pricing.html dynamic models here ----------------------------------------------------------------------
#
#
#



# start of blog.html dynamic models here ----------------------------------------------------------------------



# End of blog.html dynamic models here ----------------------------------------------------------------------
#
#
#