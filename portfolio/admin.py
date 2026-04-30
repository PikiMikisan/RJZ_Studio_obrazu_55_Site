from django.contrib import admin
from django.utils.html import format_html

from .models import AboutMe, ContactMessage, PortfolioCategory, PortfolioPhoto, SiteInfo

admin.site.site_header = "Panel administracyjny - Fotograf"
admin.site.site_title = "Fotograf CMS"
admin.site.index_title = "Zarządzaj treściami strony"


@admin.register(SiteInfo)
class SiteInfoAdmin(admin.ModelAdmin):
    list_display = ["title", "tagline", "updated_at"]
    fieldsets = (
        ("Podstawowe", {"fields": ("title", "logo", "tagline", "hero_image")}),
        ("Treść sekcji Informacje", {"fields": ("info_content",)}),
    )

    def has_add_permission(self, request):
        return not SiteInfo.objects.exists()


@admin.register(AboutMe)
class AboutMeAdmin(admin.ModelAdmin):
    list_display = ["__str__", "updated_at"]

    def has_add_permission(self, request):
        return not AboutMe.objects.exists()


@admin.register(PortfolioCategory)
class PortfolioCategoryAdmin(admin.ModelAdmin):
    list_display = ["name", "slug", "order"]
    prepopulated_fields = {"slug": ("name",)}
    ordering = ["order"]


@admin.register(PortfolioPhoto)
class PortfolioPhotoAdmin(admin.ModelAdmin):
    list_display = ["thumbnail", "title", "category", "is_featured", "order", "created_at"]
    list_display_links = ["thumbnail", "title"]
    list_filter = ["category", "is_featured"]
    list_editable = ["is_featured", "order"]
    search_fields = ["title", "description"]
    ordering = ["order", "-created_at"]

    def thumbnail(self, obj):
        if obj.image:
            return format_html(
                '<img src="{}" style="height:60px;border-radius:4px;" />',
                obj.image.url,
            )
        return "-"

    thumbnail.short_description = "Podgląd"


@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ["name", "email", "phone", "subject", "sent_at", "is_read"]
    list_filter = ["is_read"]
    search_fields = ["name", "email", "subject"]
    readonly_fields = ["name", "email", "phone", "subject", "message", "sent_at"]
    list_editable = ["is_read"]

    def has_add_permission(self, request):
        return False
