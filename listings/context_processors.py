from django.conf import settings
from django.db.models import Q


def maptiler_key(request):
    """Makes MAPTILER_API_KEY available in every template as {{ maptiler_key }}."""
    return {"maptiler_key": settings.MAPTILER_API_KEY}


def unread_message_count(request):
    """Makes {{ unread_message_count }} available in every template, for the nav badge."""
    if not request.user.is_authenticated:
        return {"unread_message_count": 0}

    from .models import Message  # local import avoids a circular import at startup

    count = Message.objects.filter(
        Q(conversation__seeker=request.user) | Q(conversation__listing__provider=request.user)
    ).exclude(sender=request.user).filter(is_read=False).count()

    return {"unread_message_count": count}
