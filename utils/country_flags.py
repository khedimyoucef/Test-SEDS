# =============================================================================
# COUNTRY FLAGS UTILITY
# =============================================================================
# This module provides functions to display country flags in the dashboard.
# 
# Note: Unicode flag emojis don't render on Windows, so we use flag images
# from flagcdn.com instead. This provides consistent rendering across all OS.
# =============================================================================

# Mapping from IOC codes to ISO 2-letter codes (needed for flag images)
# Flag CDNs use ISO 3166-1 alpha-2 codes (2 letters)
IOC_TO_ISO2 = {
    'AFG': 'af', 'ALB': 'al', 'ALG': 'dz', 'AND': 'ad', 'ANG': 'ao',
    'ANT': 'ag', 'ARG': 'ar', 'ARM': 'am', 'ARU': 'aw', 'ASA': 'as',
    'AUS': 'au', 'AUT': 'at', 'AZE': 'az', 'BAH': 'bs', 'BAN': 'bd',
    'BAR': 'bb', 'BDI': 'bi', 'BEL': 'be', 'BEN': 'bj', 'BER': 'bm',
    'BHU': 'bt', 'BIH': 'ba', 'BIZ': 'bz', 'BLR': 'by', 'BOL': 'bo',
    'BOT': 'bw', 'BRA': 'br', 'BRN': 'bh', 'BRU': 'bn', 'BUL': 'bg',
    'BUR': 'bf', 'CAF': 'cf', 'CAM': 'kh', 'CAN': 'ca', 'CAY': 'ky',
    'CGO': 'cg', 'CHA': 'td', 'CHI': 'cl', 'CHN': 'cn', 'CIV': 'ci',
    'CMR': 'cm', 'COD': 'cd', 'COK': 'ck', 'COL': 'co', 'COM': 'km',
    'CPV': 'cv', 'CRC': 'cr', 'CRO': 'hr', 'CUB': 'cu', 'CYP': 'cy',
    'CZE': 'cz', 'DEN': 'dk', 'DJI': 'dj', 'DMA': 'dm', 'DOM': 'do',
    'ECU': 'ec', 'EGY': 'eg', 'ERI': 'er', 'ESA': 'sv', 'ESP': 'es',
    'EST': 'ee', 'ETH': 'et', 'FIJ': 'fj', 'FIN': 'fi', 'FRA': 'fr',
    'FSM': 'fm', 'GAB': 'ga', 'GAM': 'gm', 'GBR': 'gb', 'GBS': 'gw',
    'GEO': 'ge', 'GEQ': 'gq', 'GER': 'de', 'GHA': 'gh', 'GRE': 'gr',
    'GRN': 'gd', 'GUA': 'gt', 'GUI': 'gn', 'GUM': 'gu', 'GUY': 'gy',
    'HAI': 'ht', 'HKG': 'hk', 'HON': 'hn', 'HUN': 'hu', 'INA': 'id',
    'IND': 'in', 'IRI': 'ir', 'IRL': 'ie', 'IRQ': 'iq', 'ISL': 'is',
    'ISR': 'il', 'ISV': 'vi', 'ITA': 'it', 'IVB': 'vg', 'JAM': 'jm',
    'JOR': 'jo', 'JPN': 'jp', 'KAZ': 'kz', 'KEN': 'ke', 'KGZ': 'kg',
    'KIR': 'ki', 'KOR': 'kr', 'KOS': 'xk', 'KSA': 'sa', 'KUW': 'kw',
    'LAO': 'la', 'LAT': 'lv', 'LBA': 'ly', 'LBN': 'lb', 'LBR': 'lr',
    'LCA': 'lc', 'LES': 'ls', 'LIE': 'li', 'LTU': 'lt', 'LUX': 'lu',
    'MAD': 'mg', 'MAR': 'ma', 'MAS': 'my', 'MAW': 'mw', 'MDA': 'md',
    'MDV': 'mv', 'MEX': 'mx', 'MGL': 'mn', 'MHL': 'mh', 'MKD': 'mk',
    'MLI': 'ml', 'MLT': 'mt', 'MNE': 'me', 'MON': 'mc', 'MOZ': 'mz',
    'MRI': 'mu', 'MTN': 'mr', 'MYA': 'mm', 'NAM': 'na', 'NCA': 'ni',
    'NED': 'nl', 'NEP': 'np', 'NGR': 'ng', 'NIG': 'ne', 'NOR': 'no',
    'NRU': 'nr', 'NZL': 'nz', 'OMA': 'om', 'PAK': 'pk', 'PAN': 'pa',
    'PAR': 'py', 'PER': 'pe', 'PHI': 'ph', 'PLE': 'ps', 'PLW': 'pw',
    'PNG': 'pg', 'POL': 'pl', 'POR': 'pt', 'PRK': 'kp', 'PUR': 'pr',
    'QAT': 'qa', 'ROU': 'ro', 'RSA': 'za', 'RUS': 'ru', 'RWA': 'rw',
    'SAM': 'ws', 'SEN': 'sn', 'SEY': 'sc', 'SGP': 'sg', 'SKN': 'kn',
    'SLE': 'sl', 'SLO': 'si', 'SMR': 'sm', 'SOL': 'sb', 'SOM': 'so',
    'SRB': 'rs', 'SRI': 'lk', 'SSD': 'ss', 'STP': 'st', 'SUD': 'sd',
    'SUI': 'ch', 'SUR': 'sr', 'SVK': 'sk', 'SWE': 'se', 'SWZ': 'sz',
    'SYR': 'sy', 'TAN': 'tz', 'TGA': 'to', 'THA': 'th', 'TJK': 'tj',
    'TKM': 'tm', 'TLS': 'tl', 'TOG': 'tg', 'TPE': 'tw', 'TTO': 'tt',
    'TUN': 'tn', 'TUR': 'tr', 'TUV': 'tv', 'UAE': 'ae', 'UGA': 'ug',
    'UKR': 'ua', 'URU': 'uy', 'USA': 'us', 'UZB': 'uz', 'VAN': 'vu',
    'VEN': 've', 'VIE': 'vn', 'VIN': 'vc', 'YEM': 'ye', 'ZAM': 'zm',
    'ZIM': 'zw',
    # Special Olympic codes - use Olympic flag or similar
    'EOR': 'un',  # Refugee Olympic Team
    'ROC': 'ru',  # Russian Olympic Committee
    'AIN': 'un',  # Individual Neutral Athletes - use UN flag
}


def get_flag_emoji(country_code):
    """
    Convert a country code to a flag emoji.
    Note: This returns Unicode flag emoji which may not render on Windows.
    For Windows compatibility, use get_flag_html() instead.
    """
    if not country_code:
        return '🏳️'
    
    # Get ISO-2 code
    if len(country_code) == 3:
        iso2 = IOC_TO_ISO2.get(country_code.upper(), '').upper()
    elif len(country_code) == 2:
        iso2 = country_code.upper()
    else:
        return '🏳️'
    
    if not iso2:
        return '🏳️'
    
    # Convert to regional indicator symbols
    flag = ''
    for char in iso2:
        flag += chr(0x1F1E6 + ord(char) - ord('A'))
    
    return flag


def get_flag_url(country_code, size=20):
    """
    Get the URL for a country flag image from flagcdn.com.
    
    Args:
        country_code: IOC or ISO country code
        size: Width of the flag image in pixels (height is auto)
    
    Returns:
        URL string to the flag image
    """
    if not country_code:
        return f"https://flagcdn.com/w{size}/un.png"
    
    # Get ISO-2 code (lowercase for the CDN)
    if len(country_code) == 3:
        iso2 = IOC_TO_ISO2.get(country_code.upper(), 'un')
    elif len(country_code) == 2:
        iso2 = country_code.lower()
    else:
        iso2 = 'un'
    
    return f"https://flagcdn.com/w{size}/{iso2}.png"


def get_flag_html(country_code, size=20):
    """
    Get an HTML img tag for a country flag.
    Use this in Streamlit with st.markdown(..., unsafe_allow_html=True)
    
    Args:
        country_code: IOC or ISO country code
        size: Width of the flag image in pixels
    
    Returns:
        HTML string with an img tag
    """
    url = get_flag_url(country_code, size)
    return f'<img src="{url}" width="{size}" style="vertical-align: middle; margin-right: 5px;">'


def get_country_with_flag(country_code, country_name=None, size=20):
    """
    Get HTML for a country name with its flag image inline.
    
    Args:
        country_code: IOC country code
        country_name: Full country name (optional, uses code if not provided)
        size: Flag image width in pixels
    
    Returns:
        HTML string with flag image and country name
    """
    flag_html = get_flag_html(country_code, size)
    display_name = country_name if country_name else country_code
    return f'{flag_html}{display_name}'
