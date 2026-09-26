# Approximate main-campus coordinates for major Zimbabwean tertiary institutions.
# Used to power "search near my campus" distance filtering on the student listings page.
# Coordinates are approximate (city-block level), which is accurate enough for a
# "how far is this from campus" filter. Add more institutions here as needed —
# each just needs a name, latitude, and longitude.

INSTITUTIONS = [
    {"name": "University of Zimbabwe (UZ)", "lat": -17.7833, "lng": 31.0500},
    {"name": "National University of Science and Technology (NUST)", "lat": -20.2350, "lng": 28.6350},
    {"name": "Midlands State University (MSU)", "lat": -19.5160, "lng": 29.8330},
    {"name": "Harare Institute of Technology (HIT)", "lat": -17.8300, "lng": 31.0100},
    {"name": "Chinhoyi University of Technology (CUT)", "lat": -17.3480, "lng": 30.1940},
    {"name": "Bindura University of Science Education (BUSE)", "lat": -17.3020, "lng": 31.3310},
    {"name": "Great Zimbabwe University (GZU)", "lat": -20.0680, "lng": 30.8280},
    {"name": "Lupane State University (LSU)", "lat": -18.9310, "lng": 27.8050},
    {"name": "Africa University (AU)", "lat": -18.9710, "lng": 32.6330},
    {"name": "Women's University in Africa (WUA)", "lat": -17.8220, "lng": 31.0490},
    {"name": "Zimbabwe Open University (ZOU)", "lat": -17.8280, "lng": 31.0410},
    {"name": "Solusi University", "lat": -19.9500, "lng": 28.4000},
    {"name": "Catholic University of Zimbabwe (CUZ)", "lat": -17.8280, "lng": 31.0530},
    {"name": "Marondera University of Agricultural Sciences and Technology (MUAST)", "lat": -18.1850, "lng": 31.5510},
    {"name": "Gwanda State University", "lat": -20.9350, "lng": 29.0000},
    {"name": "Harare Polytechnic", "lat": -17.8280, "lng": 31.0470},
    {"name": "Bulawayo Polytechnic", "lat": -20.1500, "lng": 28.5800},
    {"name": "Kwekwe Polytechnic", "lat": -18.9280, "lng": 29.8150},
    {"name": "Masvingo Polytechnic", "lat": -20.0630, "lng": 30.8300},
    {"name": "Mutare Polytechnic", "lat": -18.9700, "lng": 32.6600},
]


def get_institution(name):
    """Returns the institution dict matching this name, or None."""
    for inst in INSTITUTIONS:
        if inst["name"] == name:
            return inst
    return None
