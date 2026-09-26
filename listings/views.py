import json
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Listing, ListingImage
from .forms import ListingForm, ListingImageForm, StyledSignupForm
from .institutions import INSTITUTIONS, get_institution
from .distance import distance_km


def home(request):
    """Landing page — choose Student or General."""
    return render(request, "listings/home.html")


def listing_list(request, category):
    """
    category is 'student' or 'general' — pulled from the URL.
    Listings tagged 'both' show up in either section.
    """
    listings = Listing.objects.filter(is_active=True).filter(
        category__in=[category, "both"]
    )

    # --- Filters from query params ---
    city = request.GET.get("city")
    max_price = request.GET.get("max_price")
    listing_type = request.GET.get("listing_type")

    if city:
        listings = listings.filter(city__icontains=city)
    if max_price:
        listings = listings.filter(price__lte=max_price)
    if listing_type:
        listings = listings.filter(listing_type=listing_type)

    near_institution = None
    radius_km = None
    listings_without_location_count = 0

    # Student-only: search by distance from a chosen campus
    if category == "student":
        near_name = request.GET.get("near")
        if near_name:
            near_institution = get_institution(near_name)

        if near_institution:
            radius_km = float(request.GET.get("radius", 10))

            with_location = [l for l in listings if l.latitude is not None and l.longitude is not None]
            listings_without_location_count = listings.count() - len(with_location)

            nearby = []
            for listing in with_location:
                d = distance_km(near_institution["lat"], near_institution["lng"], listing.latitude, listing.longitude)
                if d <= radius_km:
                    listing.distance_km = round(d, 1)
                    nearby.append(listing)

            nearby.sort(key=lambda l: l.distance_km)
            listings = nearby
        else:
            # Fall back to the old free-text match when no campus is chosen from the dropdown
            institution_text = request.GET.get("institution")
            if institution_text:
                listings = listings.filter(nearest_institution__icontains=institution_text)

    context = {
        "listings": listings,
        "category": category,
        "listing_type_choices": Listing.LISTING_TYPE_CHOICES,
        "institutions": INSTITUTIONS,
        "near_institution": near_institution,
        "radius_km": radius_km,
        "listings_without_location_count": listings_without_location_count,
    }
    return render(request, "listings/listing_list.html", context)


def listing_detail(request, pk):
    listing = get_object_or_404(Listing, pk=pk, is_active=True)
    return render(request, "listings/listing_detail.html", {"listing": listing})


def signup(request):
    """Providers create an account here so they can post listings."""
    if request.method == "POST":
        form = StyledSignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Account created. You can now post a listing.")
            return redirect("listings:create_listing")
    else:
        form = StyledSignupForm()
    return render(request, "listings/signup.html", {"form": form})


@login_required
def my_listings(request):
    """A provider's own listings — edit, deactivate, or add new ones."""
    listings = Listing.objects.filter(provider=request.user)
    return render(request, "listings/my_listings.html", {"listings": listings})


@login_required
def create_listing(request):
    if request.method == "POST":
        form = ListingForm(request.POST)
        if form.is_valid():
            listing = form.save(commit=False)
            listing.provider = request.user
            listing.save()

            # Handle multiple uploaded images
            for image_file in request.FILES.getlist("images"):
                ListingImage.objects.create(listing=listing, image=image_file)

            messages.success(request, "Listing posted successfully.")
            return redirect("listings:my_listings")
    else:
        form = ListingForm()
    return render(request, "listings/listing_form.html", {"form": form, "is_edit": False})


@login_required
def edit_listing(request, pk):
    listing = get_object_or_404(Listing, pk=pk, provider=request.user)
    if request.method == "POST":
        form = ListingForm(request.POST, instance=listing)
        if form.is_valid():
            form.save()

            # Remove any existing photos the provider checked for deletion
            image_ids_to_delete = request.POST.getlist("delete_images")
            if image_ids_to_delete:
                for img in listing.images.filter(id__in=image_ids_to_delete):
                    img.image.delete(save=False)  # removes the actual file (Cloudinary or local)
                    img.delete()

            for image_file in request.FILES.getlist("images"):
                ListingImage.objects.create(listing=listing, image=image_file)

            messages.success(request, "Listing updated.")
            return redirect("listings:my_listings")
    else:
        form = ListingForm(instance=listing)
    return render(request, "listings/listing_form.html", {"form": form, "is_edit": True, "listing": listing})


@login_required
def delete_listing(request, pk):
    listing = get_object_or_404(Listing, pk=pk, provider=request.user)
    if request.method == "POST":
        listing.delete()
        messages.success(request, "Listing removed.")
        return redirect("listings:my_listings")
    return render(request, "listings/delete_confirm.html", {"listing": listing})


def map_view(request, category=None):
    """
    Shows all active listings with coordinates as pins on a map.
    category is optional: 'student', 'general', or None for all.
    """
    listings = Listing.objects.filter(
        is_active=True, latitude__isnull=False, longitude__isnull=False
    )
    if category in ("student", "general"):
        listings = listings.filter(category__in=[category, "both"])

    pins = [
        {
            "id": listing.pk,
            "title": listing.title,
            "price": str(listing.price),
            "price_period": listing.get_price_period_display(),
            "city": listing.city,
            "lat": float(listing.latitude),
            "lng": float(listing.longitude),
            "url": f"/listing/{listing.pk}/",
            "verified": listing.is_verified,
        }
        for listing in listings
    ]

    context = {
        "pins_json": json.dumps(pins),
        "category": category,
        "listing_count": len(pins),
    }
    return render(request, "listings/map.html", context)
