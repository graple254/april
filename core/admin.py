from django.contrib import admin
from .models import *
from django.utils.html import format_html

# Base ModelAdmin for common configurations
class BaseSectionAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'id')
    search_fields = [f for f in dir(HeroSection) if f.startswith('text_') or f.startswith('title_')]
    fieldsets = (
        (None, {
            'fields': [f for f in dir(HeroSection) if f.startswith('text_') or f.startswith('title_') or f in ('highlighted_title', 'basic_price', 'promise_1', 'promise_2', 'promise_3', 'promise_4', 'promise_5', 'promise_6', 'notification_text', 'subtitle_text', 'paragraph', 'affirmative_text')]
        }),
    )

    def get_fieldsets(self, request, obj=None):
        fieldsets = super().get_fieldsets(request, obj)
        # Only include fields that exist in the model
        valid_fields = [f.name for f in self.model._meta.fields]
        new_fieldsets = []
        for name, options in fieldsets:
            fields = [f for f in options['fields'] if f in valid_fields]
            if fields:
                new_fieldsets.append((name, {'fields': fields}))
        return new_fieldsets

# Inline for Brands related to Brands_we_work_with
class BrandsInline(admin.TabularInline):
    model = Brands
    extra = 1
    fields = ('brand_name', 'brand_bi_bi')
    search_fields = ('brand_name', 'brand_bi_bi')

@admin.register(HeroSection)
class HeroSectionAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'main_title_1', 'highlighted_title')

@admin.register(Why_jadoo)
class WhyJadooAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'text_title_1', 'text_title_2', 'text_title_3')

@admin.register(How_it_works)
class HowItWorksAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'text_title_1', 'text_title_2', 'text_title_3')

@admin.register(business_proposition)
class BusinessPropositionAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'text_title_1', 'text_title_2')

@admin.register(business_proposition_modal)
class BusinessPropositionModalAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'card_title_1', 'basic_price')

@admin.register(Brands_we_work_with)
class BrandsWeWorkWithAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'text_title_1', 'text_title_2')
    inlines = [BrandsInline]

@admin.register(cretor_proposition)
class CreatorPropositionAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'text_title_1', 'text_title_2')

@admin.register(creator_proposition_modal)
class CreatorPropositionModalAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'card_title_1', 'card_title_2')

@admin.register(Privacy_policy)
class PrivacyPolicyAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'text_title_1')

@admin.register(Terms_and_conditions)
class TermsAndConditionsAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'text_title_1')

@admin.register(refund_policy)
class RefundPolicyAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'text_title_1')

@admin.register(Contact_us)
class ContactUsAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'whatsapp_number', 'email')
    search_fields = ('whatsapp_number', 'email')
    fields = ('whatsapp_number', 'email')

@admin.register(Blog)
class BlogAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'title_1', 'summary_text')
    search_fields = ('title_1', 'summary_text', 'full_text')

# Register Brands separately if needed
@admin.register(Brands)
class BrandsAdmin(admin.ModelAdmin):
    list_display = ('brand_name', 'brands', 'brand_bi_bi')
    search_fields = ('brand_name', 'brand_bi_bi')
    list_filter = ('brands',)


@admin.register(SEOMetaTag)
class SEOMetaTagAdmin(admin.ModelAdmin):
    list_display = ("dc_title", "author", "updated_at")
    search_fields = ("dc_title", "author", "dc_subject", "keywords")
    readonly_fields = ("updated_at",)
    
    fieldsets = (
        ("Standard Meta Tags", {
            "fields": ("description", "author", "keywords", "robots")
        }),
        ("Dublin Core Metadata", {
            "fields": (
                "dc_title", "dc_description", "dc_creator", "dc_publisher",
                "dc_subject", "dc_type", "dc_format", "dc_language", "dc_rights"
            )
        }),
        ("Timestamps", {
            "fields": ("updated_at",),
            "classes": ("collapse",),
        }),
    )

    def has_add_permission(self, request):
        # Limit to only 1 SEO object (singleton pattern)
        if SEOMetaTag.objects.exists():
            return False
        return super().has_add_permission(request)    
    

@admin.register(Visitor)
class VisitorAdmin(admin.ModelAdmin):
    list_display = (
        'ip_address',
        'location',
        'short_path',
        'method',
        'referrer_link',
        'formatted_user_agent',
        'visit_date',
    )
    list_filter = ('method', 'visit_date', 'location')
    search_fields = ('ip_address', 'location', 'user_agent', 'url_path', 'referrer')
    ordering = ('-visit_date',)
    readonly_fields = [field.name for field in Visitor._meta.fields]
    list_per_page = 50

    def short_path(self, obj):
        return (obj.url_path[:40] + '...') if len(obj.url_path or '') > 40 else obj.url_path
    short_path.short_description = 'URL Path'

    def referrer_link(self, obj):
        if obj.referrer:
            return format_html('<a href="{0}" target="_blank">{0}</a>', obj.referrer)
        return '-'
    referrer_link.short_description = 'Referrer'

    def formatted_user_agent(self, obj):
        return (obj.user_agent[:40] + '...') if len(obj.user_agent or '') > 40 else obj.user_agent
    formatted_user_agent.short_description = 'User Agent'

    def has_add_permission(self, request):
        return False  # Visitors should only be created by middleware, not manually

    def has_change_permission(self, request, obj=None):
        return False  # Lock records for audit integrity

    def has_delete_permission(self, request, obj=None):
        return True  # Allow cleanup if needed    

