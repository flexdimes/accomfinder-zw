from django.db import models
from django.contrib.auth.models import User


class Listing(models.Model):
    CATEGORY_CHOICES = [
        ("student", "Student Boarding"),
        ("general", "General Accommodation"),
        ("both", "Both"),
    ]

    LISTING_TYPE_CHOICES = [
        ("room_shared", "Shared Room"),
        ("room_single", "Single Room"),
        ("cottage", "Cottage"),
        ("flat", "Flat/Apartment"),
        ("house", "Full House"),
    ]

    PRICE_PERIOD_CHOICES = [
        ("per_month", "Per Month"),
        ("per_semester", "Per Semester"),
        ("per_year", "Per Year"),
    ]

    # Ownership
    provider = models.ForeignKey(User, on_delete=models.CASCADE, related_name="listings")

    # Core info
    title = models.CharField(max_length=200)
    description = models.TextField()
    category = models.CharField(max_length=10, choices=CATEGORY_CHOICES, default="general")
    listing_type = models.CharField(max_length=20, choices=LISTING_TYPE_CHOICES)

    # Location
    city = models.CharField(max_length=100)  # e.g. Harare, Bulawayo
    suburb = models.CharField(max_length=100, blank=True)
    nearest_institution = models.CharField(
        max_length=150, blank=True,
        help_text="e.g. University of Zimbabwe, NUST — only relevant for student category"
    )
    address_detail = models.CharField(max_length=255, blank=True)
    latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)

    # Pricing
    price = models.DecimalField(max_digits=10, decimal_places=2)
    price_period = models.CharField(max_length=20, choices=PRICE_PERIOD_CHOICES, default="per_month")

    # Student-specific
    meals_included = models.BooleanField(default=False)
    gender_specific = models.CharField(
        max_length=10,
        choices=[("male", "Male only"), ("female", "Female only"), ("mixed", "Mixed/Any")],
        default="mixed",
    )

    # Shared-room specific — how many people the room fits, and how many spots are taken
    room_capacity = models.PositiveIntegerField(
        null=True, blank=True,
        help_text="Total number of people this room fits (only relevant for Shared Room listings)"
    )
    occupied_spots = models.PositiveIntegerField(
        null=True, blank=True, default=0,
        help_text="How many of those spots are currently taken"
    )

    # General-specific
    pets_allowed = models.BooleanField(default=False)
    utilities_included = models.BooleanField(default=False)

    # Trust / verification
    is_verified = models.BooleanField(default=False)
    contact_whatsapp = models.CharField(max_length=20, help_text="e.g. 263771234567 (no + or spaces)")

    # Meta
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.title} ({self.get_category_display()})"

    @property
    def whatsapp_link(self):
        return f"https://wa.me/{self.contact_whatsapp}"

    @property
    def spots_left(self):
        """Only meaningful for shared rooms with a capacity set. Returns None otherwise."""
        if self.listing_type != "room_shared" or self.room_capacity is None:
            return None
        occupied = self.occupied_spots or 0
        return max(self.room_capacity - occupied, 0)

    @property
    def is_full(self):
        left = self.spots_left
        return left is not None and left <= 0


class ListingImage(models.Model):
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="images")
    image = models.ImageField(upload_to="listing_images/")
    is_primary = models.BooleanField(default=False)

    def __str__(self):
        return f"Image for {self.listing.title}"
