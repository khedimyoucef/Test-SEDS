# Approximate coordinates for Paris 2024 Venues
VENUE_COORDINATES = {
    "Aquatics Centre": {"lat": 48.9244, "lon": 2.3600},
    "Bercy Arena": {"lat": 48.8386, "lon": 2.3785},
    "Bordeaux Stadium": {"lat": 44.8969, "lon": -0.5639},
    "Champ de Mars Arena": {"lat": 48.8530, "lon": 2.3012},
    "Château de Versailles": {"lat": 48.8049, "lon": 2.1204},
    "Chateauroux Shooting Centre": {"lat": 46.8115, "lon": 1.7534},
    "Eiffel Tower Stadium": {"lat": 48.8584, "lon": 2.2945},
    "Elancourt Hill": {"lat": 48.7708, "lon": 1.9667},
    "Geoffroy-Guichard Stadium": {"lat": 45.4608, "lon": 4.3903},
    "Grand Palais": {"lat": 48.8661, "lon": 2.3125},
    "Hôtel de Ville": {"lat": 48.8566, "lon": 2.3522},
    "Invalides": {"lat": 48.8622, "lon": 2.3125},
    "La Beaujoire Stadium": {"lat": 47.2556, "lon": -1.5253},
    "La Concorde": {"lat": 48.8656, "lon": 2.3212},
    "Le Bourget Sport Climbing Venue": {"lat": 48.9394, "lon": 2.4250},
    "Golf National": {"lat": 48.7547, "lon": 2.0744},
    "Lyon Stadium": {"lat": 45.7653, "lon": 4.9820},
    "Marseille Marina": {"lat": 43.2700, "lon": 5.3692},
    "Marseille Stadium": {"lat": 43.2699, "lon": 5.3959},
    "Nice Stadium": {"lat": 43.7056, "lon": 7.1925},
    "North Paris Arena": {"lat": 48.9719, "lon": 2.4861},
    "Parc des Princes": {"lat": 48.8414, "lon": 2.2530},
    "Paris La Defense Arena": {"lat": 48.8958, "lon": 2.2297},
    "Pierre Mauroy Stadium": {"lat": 50.6119, "lon": 3.1305},
    "Pont Alexandre III": {"lat": 48.8639, "lon": 2.3136},
    "Porte de La Chapelle Arena": {"lat": 48.8994, "lon": 2.3611},
    "Stade Roland-Garros": {"lat": 48.8473, "lon": 2.2494},
    "Saint-Quentin-en-Yvelines BMX Stadium": {"lat": 48.7844, "lon": 2.0311},
    "Saint-Quentin-en-Yvelines Velodrome": {"lat": 48.7844, "lon": 2.0311},
    "South Paris Arena": {"lat": 48.8322, "lon": 2.2856},
    "Stade de France": {"lat": 48.9245, "lon": 2.3602},
    "Teahupo'o, Tahiti": {"lat": -17.8472, "lon": -149.2667},
    "Trocadéro": {"lat": 48.8616, "lon": 2.2893},
    "Vaires-sur-Marne Nautical Stadium": {"lat": 48.8625, "lon": 2.6378},
    "Yves-du-Manoir Stadium": {"lat": 48.9292, "lon": 2.2475},
    
    # Aliases / Variations found in data
    "La Chapelle Arena": {"lat": 48.8994, "lon": 2.3611}, # Porte de La Chapelle Arena
    "South Paris Arena 1": {"lat": 48.8322, "lon": 2.2856},
    "South Paris Arena 4": {"lat": 48.8322, "lon": 2.2856},
    "South Paris Arena 6": {"lat": 48.8322, "lon": 2.2856},
    "Nautical St - Flat water": {"lat": 48.8625, "lon": 2.6378}, # Vaires-sur-Marne
    "Nautical St - White water": {"lat": 48.8625, "lon": 2.6378}, # Vaires-sur-Marne
    "Chateauroux Shooting Ctr": {"lat": 46.8115, "lon": 1.7534},
    "Champ-de-Mars Arena": {"lat": 48.8530, "lon": 2.3012},
    "Roland-Garros Stadium": {"lat": 48.8473, "lon": 2.2494}
}

def get_venue_coordinates(venue_name):
    """Returns a tuple (lat, lon) for a given venue name, or None if not found."""
    coords = VENUE_COORDINATES.get(venue_name)
    if coords:
        return coords['lat'], coords['lon']
    return None
