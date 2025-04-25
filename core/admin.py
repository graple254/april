from django.contrib import admin
from .models import (
    HeroSection,
    Why_jadoo,
    How_it_works,
    Brands_we_work_with,
    Brands,
    cretor_invitation_card,
    Privacy_policy,
    Terms_and_conditions,
)


# Inline for Brands to manage within Brands_we_work_with
class BrandsInline(admin.TabularInline):
    model = Brands
    extra = 1  # Number of empty forms to display
    fields = ['brand_name', 'brand_bi_bi']
    verbose_name = "Brand"
    verbose_name_plural = "Brands"


@admin.register(HeroSection)
class HeroSectionAdmin(admin.ModelAdmin):
    list_display = ['id', 'main_title_1', 'highlighted_title']
    fieldsets = (
        (None, {
            'fields': (
                'main_title_1',
                'main_title_2',
                'highlighted_title',
                'text_1',
                'text_2',
                'text_3',
                'text_4',
                'affirmative_text',
            )
        }),
    )


@admin.register(Why_jadoo)
class WhyJadooAdmin(admin.ModelAdmin):
    list_display = ['id', 'text_title_1', 'text_title_2']
    fieldsets = (
        (None, {
            'fields': (
                'text_title_1',
                'text_title_2',
                'text_title_3',
                'text_title_4',
                'text_title_5',
                'paragraph',
            )
        }),
    )


@admin.register(How_it_works)
class HowItWorksAdmin(admin.ModelAdmin):
    list_display = ['id', 'text_title_1', 'text_title_2', 'text_title_3']
    fieldsets = (
        ('Section Title and Subtitle', {
            'fields': (
                'text_title_1',
                'text_title_2',
                'text_title_3',
                'subtitle_text',
            )
        }),
        ('Create a Campaign', {
            'fields': (
                'sub_title_1',
                'sb1_text_1',
                'sb1_text_2',
                'listing_1',
                'listing_1_text',
                'listing_2',
                'listing_2_text',
            )
        }),
        ('Set a Budget', {
            'fields': (
                'sub_title_2',
                'sb2_text_1',
                'sb2_text_2',
                'sb2_text_3',
                'detail_text_1',
                'dt_1',
                'dt_1_text',
                'dt_2',
                'dt_2_text',
                'dt_3',
                'dt_3_text',
                'closing_text',
            )
        }),
        ('Reach the Right Creators', {
            'fields': (
                'sub_title_3',
                'sb3_text_1',
            )
        }),
        ('Track Real Impact', {
            'fields': (
                'sub_title_4',
                'sb4_text_1',
            )
        }),
    )


@admin.register(Brands_we_work_with)
class BrandsWeWorkWithAdmin(admin.ModelAdmin):
    list_display = ['id', 'text_title_1', 'text_title_2']
    inlines = [BrandsInline]
    fieldsets = (
        (None, {
            'fields': (
                'text_title_1',
                'text_title_2',
            )
        }),
    )


@admin.register(Brands)
class BrandsAdmin(admin.ModelAdmin):
    list_display = ['brand_name', 'brands', 'brand_bi_bi']
    list_filter = ['brands']
    search_fields = ['brand_name', 'brand_bi_bi']
    fieldsets = (
        (None, {
            'fields': (
                'brands',
                'brand_name',
                'brand_bi_bi',
            )
        }),
    )


@admin.register(cretor_invitation_card)
class CreatorInvitationCardAdmin(admin.ModelAdmin):
    list_display = ['id', 'text_title_1', 'text_title_2']
    fieldsets = (
        (None, {
            'fields': (
                'text_title_1',
                'text_title_2',
            )
        }),
    )


@admin.register(Privacy_policy)
class PrivacyPolicyAdmin(admin.ModelAdmin):
    list_display = ['id', 'text_title_1']
    fieldsets = (
        (None, {
            'fields': (
                'text_title_1',
                'text',
            )
        }),
    )


@admin.register(Terms_and_conditions)
class TermsAndConditionsAdmin(admin.ModelAdmin):
    list_display = ['id', 'text_title_1']
    fieldsets = (
        (None, {
            'fields': (
                'text_title_1',
                'text',
            )
        }),
    )