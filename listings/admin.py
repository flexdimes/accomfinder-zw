from django.contrib import admin
from .models import Listing, ListingImage


class ListingImageInline(admin.TabularInline):
    model = ListingImage
    extra = 1


@admin.register(Listing)
class ListingAdmin(admin.ModelAdmin):
    list_display = ("title", "category", "city", "price", "is_verified", "is_active", "created_at")
    list_filter = ("category", "city", "is_verified", "is_active")
    search_fields = ("title", "city", "nearest_institution")
    inlines = [ListingImageInline]
