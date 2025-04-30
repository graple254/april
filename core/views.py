from django.shortcuts import render
from .models import *


def index(request):
    context = {
        "hero_section": HeroSection.objects.first(),
        "why_jadoo": Why_jadoo.objects.first(),
        "how_it_works": How_it_works.objects.first(),
        "business_proposition": business_proposition.objects.first(),
        "business_proposition_modal": business_proposition_modal.objects.first(),
        "brands_we_work_with": Brands_we_work_with.objects.first(),
        "brands": Brands.objects.all(),
        "creator_proposition": cretor_proposition.objects.first(),
        "creator_proposition_modal": creator_proposition_modal.objects.first(),
        "privacy_policy": Privacy_policy.objects.first(),
        "terms_and_conditions": Terms_and_conditions.objects.first(),
        "refund_policy": refund_policy.objects.first(),
        "contact_us": Contact_us.objects.first(),
        "blogs": Blog.objects.all().order_by("-created_at"),
        "seo": SEOMetaTag.objects.first(),
    }

    return render(request, 'landing/index.html', context)
