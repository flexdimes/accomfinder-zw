from django.contrib import admin
from .models import Listing, ListingImage, Review, Conversation, Message


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


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ("listing", "user", "rating", "created_at")
    list_filter = ("rating",)
    search_fields = ("listing__title", "user__username", "comment")


class MessageInline(admin.TabularInline):
    model = Message
    extra = 0
    readonly_fields = ("sender", "text", "created_at", "is_read")
    can_delete = True


@admin.register(Conversation)
class ConversationAdmin(admin.ModelAdmin):
    list_display = ("listing", "seeker", "created_at")
    search_fields = ("listing__title", "seeker__username")
    inlines = [MessageInline]
