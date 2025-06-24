from django.contrib import admin
from .models import *

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('image',)
    search_fields = ('image',)
    readonly_fields = ('image',)

    def has_add_permission(self, request):
        return not Profile.objects.exists()

    def has_delete_permission(self, request, obj=None):
        return False
    
    
@admin.register(Visitor)
class VisitorAdmin(admin.ModelAdmin):
    list_display = ('ip_address', 'url_path', 'method', 'visit_date', 'location')
    list_filter = ('method', 'visit_date')
    search_fields = ('ip_address', 'url_path', 'referrer', 'user_agent')
    readonly_fields = ('visit_date',)
    ordering = ('-visit_date',)


@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ('whatsapp_number', 'email')
    search_fields = ('whatsapp_number', 'email')


@admin.register(hero)
class HeroAdmin(admin.ModelAdmin):
    list_display = ('title', 'launch_date')
    search_fields = ('title', 'subtitle')
    list_filter = ('launch_date',)
    ordering = ('-launch_date',)


@admin.register(platform_detail)
class PlatformDetailAdmin(admin.ModelAdmin):
    list_display = ('title', 'attached_hero')
    search_fields = ('title', 'subtitle', 'attached__title')

    def attached_hero(self, obj):
        return obj.attached.title if obj.attached else '-'
    attached_hero.short_description = 'Hero'


@admin.register(detail)
class DetailAdmin(admin.ModelAdmin):
    list_display = ('title', 'attached_platform')
    search_fields = ('title', 'subtitle', 'attached__title')

    def attached_platform(self, obj):
        return obj.attached.title if obj.attached else '-'
    attached_platform.short_description = 'Platform'


@admin.register(social_media)
class SocialMediaAdmin(admin.ModelAdmin):
    list_display = ('twitter', 'facebook', 'instagram', 'youtube', 'tiktok', 'linkedin')
    search_fields = ('twitter', 'facebook', 'instagram', 'youtube', 'tiktok', 'linkedin')


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('email', 'content', 'timestamp')
    search_fields = ('email', 'content')
    list_filter = ('timestamp',)
    ordering = ('-timestamp',)
