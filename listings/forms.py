from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import Listing, ListingImage


def _style_fields(form):
    for field in form.fields.values():
        field.widget.attrs["class"] = "border border-gray-300 rounded px-3 py-2 text-sm w-full"


class StyledSignupForm(UserCreationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        _style_fields(self)


class StyledLoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        _style_fields(self)


class ListingForm(forms.ModelForm):
    class Meta:
        model = Listing
        fields = [
            "title", "description", "category", "listing_type",
            "city", "suburb", "nearest_institution", "address_detail",
            "latitude", "longitude",
            "price", "price_period",
            "meals_included", "gender_specific",
            "room_capacity", "occupied_spots",
            "pets_allowed", "utilities_included",
            "contact_whatsapp",
        ]
        widgets = {
            "description": forms.Textarea(attrs={"rows": 4}),
            "latitude": forms.HiddenInput(),
            "longitude": forms.HiddenInput(),
        }
        labels = {
            "room_capacity": "Total people the room fits",
            "occupied_spots": "Spots already taken",
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        base_classes = "border border-gray-300 rounded px-3 py-2 text-sm w-full"
        for field in self.fields.values():
            widget = field.widget
            if isinstance(widget, (forms.CheckboxInput,)):
                widget.attrs["class"] = "mr-2"
            else:
                widget.attrs["class"] = base_classes


class ListingImageForm(forms.ModelForm):
    class Meta:
        model = ListingImage
        fields = ["image"]
