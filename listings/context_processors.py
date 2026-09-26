from django.conf import settings


def maptiler_key(request):
    """Makes MAPTILER_API_KEY available in every template as {{ maptiler_key }}."""
    return {"maptiler_key": settings.MAPTILER_API_KEY}
