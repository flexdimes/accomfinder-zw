from math import radians, sin, cos, sqrt, atan2


def distance_km(lat1, lng1, lat2, lng2):
    """
    Great-circle distance between two lat/lng points, in kilometers.
    Accurate for this use case (finding nearby listings) even though it
    treats the Earth as a perfect sphere.
    """
    R = 6371.0  # Earth's radius in km

    lat1, lng1, lat2, lng2 = map(radians, [float(lat1), float(lng1), float(lat2), float(lng2)])
    dlat = lat2 - lat1
    dlng = lng2 - lng1

    a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlng / 2) ** 2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))

    return R * c
