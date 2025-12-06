# =============================================================================
# VENUE COORDINATES UTILITY
# =============================================================================
# This module provides geographic coordinates (latitude and longitude) for
# the Paris 2024 Olympic venues. These coordinates are used to plot venues
# on interactive maps in the dashboard.
# 
# Note: These coordinates are approximate and were manually researched.
# The venues.csv file may not include coordinates, so we provide them here.
# =============================================================================

# Dictionary of venue coordinates
# Keys are venue names (must match exactly what appears in the schedule data)
# Values are dictionaries with 'lat' (latitude) and 'lon' (longitude)
# Latitude: positive = North, negative = South
# Longitude: positive = East, negative = West
VENUE_COORDINATES = {
    # Major Paris venues
    "Aquatics Centre": {"lat": 48.9244, "lon": 2.3600},  # Swimming, diving, water polo
    "Bercy Arena": {"lat": 48.8386, "lon": 2.3785},  # Gymnastics, basketball
    "Bordeaux Stadium": {"lat": 44.8969, "lon": -0.5639},  # Football matches (outside Paris)
    "Champ de Mars Arena": {"lat": 48.8530, "lon": 2.3012},  # Judo, wrestling
    "Château de Versailles": {"lat": 48.8049, "lon": 2.1204},  # Equestrian, modern pentathlon
    "Chateauroux Shooting Centre": {"lat": 46.8115, "lon": 1.7534},  # Shooting sports
    
    # Iconic Paris locations
    "Eiffel Tower Stadium": {"lat": 48.8584, "lon": 2.2945},  # Beach volleyball
    "Elancourt Hill": {"lat": 48.7708, "lon": 1.9667},  # Mountain biking
    "Geoffroy-Guichard Stadium": {"lat": 45.4608, "lon": 4.3903},  # Football (Saint-Étienne)
    "Grand Palais": {"lat": 48.8661, "lon": 2.3125},  # Fencing, taekwondo
    "Hôtel de Ville": {"lat": 48.8566, "lon": 2.3522},  # Paris City Hall - marathon finish
    "Invalides": {"lat": 48.8622, "lon": 2.3125},  # Archery, road cycling start/finish
    
    # More Paris venues
    "La Beaujoire Stadium": {"lat": 47.2556, "lon": -1.5253},  # Football (Nantes)
    "La Concorde": {"lat": 48.8656, "lon": 2.3212},  # 3x3 basketball, BMX, skateboarding, breaking
    "Le Bourget Sport Climbing Venue": {"lat": 48.9394, "lon": 2.4250},  # Sport climbing
    "Golf National": {"lat": 48.7547, "lon": 2.0744},  # Golf
    "Lyon Stadium": {"lat": 45.7653, "lon": 4.9820},  # Football
    
    # Marseille venues (sailing)
    "Marseille Marina": {"lat": 43.2700, "lon": 5.3692},  # Sailing events
    "Marseille Stadium": {"lat": 43.2699, "lon": 5.3959},  # Football matches
    
    # Other regional venues
    "Nice Stadium": {"lat": 43.7056, "lon": 7.1925},  # Football
    "North Paris Arena": {"lat": 48.9719, "lon": 2.4861},  # Boxing, modern pentathlon (fencing)
    "Parc des Princes": {"lat": 48.8414, "lon": 2.2530},  # Football
    "Paris La Defense Arena": {"lat": 48.8958, "lon": 2.2297},  # Swimming, water polo
    "Pierre Mauroy Stadium": {"lat": 50.6119, "lon": 3.1305},  # Basketball (Lille), handball
    "Pont Alexandre III": {"lat": 48.8639, "lon": 2.3136},  # Triathlon, open water swimming
    "Porte de La Chapelle Arena": {"lat": 48.8994, "lon": 2.3611},  # Badminton, rhythmic gymnastics
    
    # Tennis and more
    "Stade Roland-Garros": {"lat": 48.8473, "lon": 2.2494},  # Tennis, boxing
    "Saint-Quentin-en-Yvelines BMX Stadium": {"lat": 48.7844, "lon": 2.0311},  # BMX racing
    "Saint-Quentin-en-Yvelines Velodrome": {"lat": 48.7844, "lon": 2.0311},  # Track cycling
    "South Paris Arena": {"lat": 48.8322, "lon": 2.2856},  # Handball, volleyball, table tennis
    "Stade de France": {"lat": 48.9245, "lon": 2.3602},  # Athletics, rugby sevens
    
    # Special locations
    "Teahupo'o, Tahiti": {"lat": -17.8472, "lon": -149.2667},  # Surfing (French Polynesia!)
    "Trocadéro": {"lat": 48.8616, "lon": 2.2893},  # Road cycling, marathon
    "Vaires-sur-Marne Nautical Stadium": {"lat": 48.8625, "lon": 2.6378},  # Rowing, canoe/kayak
    "Yves-du-Manoir Stadium": {"lat": 48.9292, "lon": 2.2475},  # Field hockey
    
    # Aliases / Variations found in data
    # Sometimes the schedule data uses slightly different venue names
    # These aliases map to the same coordinates as their parent venues
    "La Chapelle Arena": {"lat": 48.8994, "lon": 2.3611}, # Porte de La Chapelle Arena
    "South Paris Arena 1": {"lat": 48.8322, "lon": 2.2856},  # Different halls of South Paris Arena
    "South Paris Arena 4": {"lat": 48.8322, "lon": 2.2856},
    "South Paris Arena 6": {"lat": 48.8322, "lon": 2.2856},
    "Nautical St - Flat water": {"lat": 48.8625, "lon": 2.6378}, # Vaires-sur-Marne
    "Nautical St - White water": {"lat": 48.8625, "lon": 2.6378}, # Vaires-sur-Marne
    "Chateauroux Shooting Ctr": {"lat": 46.8115, "lon": 1.7534},  # Abbreviated name
    "Champ-de-Mars Arena": {"lat": 48.8530, "lon": 2.3012},  # With hyphen
    "Roland-Garros Stadium": {"lat": 48.8473, "lon": 2.2494}  # Alternative name
}


def get_venue_coordinates(venue_name):
    """
    Get the geographic coordinates for a given venue name.
    
    This function looks up a venue by name and returns its latitude and
    longitude, which can be used to plot the venue on a map.
    
    Args:
        venue_name: The name of the venue as it appears in the schedule data.
                   Must match exactly (case-sensitive) to one of the keys
                   in VENUE_COORDINATES.
    
    Returns:
        tuple: A tuple of (latitude, longitude) if the venue is found.
              Both values are floats representing decimal degrees.
        None: If the venue name is not found in our coordinates database.
    
    Example:
        >>> get_venue_coordinates("Stade de France")
        (48.9245, 2.3602)
        >>> get_venue_coordinates("Unknown Venue")
        None
    """
    # Look up the venue in our dictionary
    coords = VENUE_COORDINATES.get(venue_name)
    
    if coords:
        # Return as a tuple (lat, lon) for easy unpacking
        return coords['lat'], coords['lon']
    
    # Return None if the venue wasn't found
    return None
