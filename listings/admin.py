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
    actions = ["mark_verified", "mark_unverified"]

    @admin.action(description="Mark selected listings as verified")
    def mark_verified(self, request, queryset):
        updated = queryset.update(is_verified=True)
        self.message_user(request, f"{updated} listing(s) marked as verified.")

    @admin.action(description="Mark selected listings as NOT verified")
    def mark_unverified(self, request, queryset):
        updated = queryset.update(is_verified=False)
        self.message_user(request, f"{updated} listing(s) marked as not verified.")
