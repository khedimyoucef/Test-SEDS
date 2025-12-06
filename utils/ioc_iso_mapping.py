# =============================================================================
# IOC TO ISO CODE MAPPING
# =============================================================================
# This module provides a mapping between IOC (International Olympic Committee)
# country codes and ISO 3166-1 alpha-3 country codes.
# 
# Why is this needed?
# - The Olympics data uses IOC codes (like 'GER' for Germany, 'SUI' for Switzerland)
# - Plotly maps use ISO 3166-1 alpha-3 codes (like 'DEU' for Germany, 'CHE' for Switzerland)
# - This mapping allows us to create choropleth maps with the Olympics data
# 
# Many IOC codes are the same as ISO codes (like 'USA', 'JPN', 'FRA'), but about
# 30% differ. This dictionary contains all Olympic countries and their mappings.
# =============================================================================

# The main mapping dictionary from IOC codes to ISO codes
# Keys are IOC codes (used in the Olympics data)
# Values are ISO 3166-1 alpha-3 codes (used by Plotly maps)
IOC_TO_ISO = {
    # Most common case: IOC and ISO codes are the same
    'AFG': 'AFG',  # Afghanistan
    'ALB': 'ALB',  # Albania
    
    # Cases where IOC and ISO codes differ:
    'ALG': 'DZA',  # Algeria - IOC uses historical French abbreviation
    
    'AND': 'AND',  # Andorra
    'ANG': 'AGO',  # Angola
    
    # Note about ANT: This is Antigua and Barbuda (ATG in ISO)
    # The old ANT code was for Netherlands Antilles which no longer exists
    'ANT': 'ATG', # Antigua and Barbuda (Note: ANT was Neth Antilles, but often confused. Check dataset.)
    # Actually, ANT in dataset is "Antigua and Barbuda" -> ATG.
    # Wait, let's check nocs.csv for ANT.
    # ANT,Antigua and Barbuda,Antigua and Barbuda,antigua-and-barbuda,P
    # So ANT -> ATG.
    
    'ARG': 'ARG',  # Argentina
    'ARM': 'ARM',  # Armenia
    'ARU': 'ABW',  # Aruba
    'ASA': 'ASM',  # American Samoa
    'AUS': 'AUS',  # Australia
    'AUT': 'AUT',  # Austria
    'AZE': 'AZE',  # Azerbaijan
    'BAH': 'BHS',  # Bahamas
    'BAN': 'BGD',  # Bangladesh
    'BAR': 'BRB',  # Barbados
    'BDI': 'BDI',  # Burundi
    'BEL': 'BEL',  # Belgium
    'BEN': 'BEN',  # Benin
    'BER': 'BMU',  # Bermuda
    'BHU': 'BTN',  # Bhutan
    'BIH': 'BIH',  # Bosnia and Herzegovina
    'BIZ': 'BLZ',  # Belize
    'BLR': 'BLR',  # Belarus
    'BOL': 'BOL',  # Bolivia
    'BOT': 'BWA',  # Botswana
    'BRA': 'BRA',  # Brazil
    'BRN': 'BHR', # Bahrain - IOC uses BRN, ISO uses BHR
    'BRU': 'BRN', # Brunei Darussalam - Confusingly, ISO uses BRN for Brunei!
    'BUL': 'BGR',  # Bulgaria
    'BUR': 'BFA',  # Burkina Faso
    'CAF': 'CAF',  # Central African Republic
    'CAM': 'KHM',  # Cambodia
    'CAN': 'CAN',  # Canada
    'CAY': 'CYM',  # Cayman Islands
    'CGO': 'COG',  # Congo
    'CHA': 'TCD',  # Chad
    'CHI': 'CHL',  # Chile
    'CHN': 'CHN',  # China
    'CIV': 'CIV',  # Côte d'Ivoire
    'CMR': 'CMR',  # Cameroon
    'COD': 'COD',  # Democratic Republic of the Congo
    'COK': 'COK',  # Cook Islands
    'COL': 'COL',  # Colombia
    'COM': 'COM',  # Comoros
    'CPV': 'CPV',  # Cape Verde
    'CRC': 'CRI',  # Costa Rica
    'CRO': 'HRV',  # Croatia
    'CUB': 'CUB',  # Cuba
    'CYP': 'CYP',  # Cyprus
    'CZE': 'CZE',  # Czech Republic
    'DEN': 'DNK',  # Denmark
    'DJI': 'DJI',  # Djibouti
    'DMA': 'DMA',  # Dominica
    'DOM': 'DOM',  # Dominican Republic
    'ECU': 'ECU',  # Ecuador
    'EGY': 'EGY',  # Egypt
    'ERI': 'ERI',  # Eritrea
    'ESA': 'SLV',  # El Salvador
    'ESP': 'ESP',  # Spain
    'EST': 'EST',  # Estonia
    'ETH': 'ETH',  # Ethiopia
    'FIJ': 'FJI',  # Fiji
    'FIN': 'FIN',  # Finland
    'FRA': 'FRA',  # France
    'FSM': 'FSM',  # Micronesia
    'GAB': 'GAB',  # Gabon
    'GAM': 'GMB',  # Gambia
    'GBR': 'GBR',  # Great Britain
    'GBS': 'GNB',  # Guinea-Bissau
    'GEO': 'GEO',  # Georgia
    'GEQ': 'GNQ',  # Equatorial Guinea
    'GER': 'DEU',  # Germany - IOC uses historical abbreviation
    'GHA': 'GHA',  # Ghana
    'GRE': 'GRC',  # Greece
    'GRN': 'GRD',  # Grenada
    'GUA': 'GTM',  # Guatemala
    'GUI': 'GIN',  # Guinea
    'GUM': 'GUM',  # Guam
    'GUY': 'GUY',  # Guyana
    'HAI': 'HTI',  # Haiti
    'HKG': 'HKG',  # Hong Kong
    'HON': 'HND',  # Honduras
    'HUN': 'HUN',  # Hungary
    'INA': 'IDN',  # Indonesia
    'IND': 'IND',  # India
    'IRI': 'IRN',  # Iran
    'IRL': 'IRL',  # Ireland
    'IRQ': 'IRQ',  # Iraq
    'ISL': 'ISL',  # Iceland
    'ISR': 'ISR',  # Israel
    'ISV': 'VIR',  # US Virgin Islands
    'ITA': 'ITA',  # Italy
    'IVB': 'VGB',  # British Virgin Islands
    'JAM': 'JAM',  # Jamaica
    'JOR': 'JOR',  # Jordan
    'JPN': 'JPN',  # Japan
    'KAZ': 'KAZ',  # Kazakhstan
    'KEN': 'KEN',  # Kenya
    'KGZ': 'KGZ',  # Kyrgyzstan
    'KIR': 'KIR',  # Kiribati
    'KOR': 'KOR',  # South Korea
    'KOS': 'XKX', # Kosovo - Uses XKX as placeholder (no official ISO code)
    'KSA': 'SAU',  # Saudi Arabia
    'KUW': 'KWT',  # Kuwait
    'LAO': 'LAO',  # Laos
    'LAT': 'LVA',  # Latvia
    'LBA': 'LBY',  # Libya
    'LBN': 'LBN',  # Lebanon
    'LBR': 'LBR',  # Liberia
    'LCA': 'LCA',  # Saint Lucia
    'LES': 'LSO',  # Lesotho
    'LIE': 'LIE',  # Liechtenstein
    'LTU': 'LTU',  # Lithuania
    'LUX': 'LUX',  # Luxembourg
    'MAD': 'MDG',  # Madagascar
    'MAR': 'MAR',  # Morocco
    'MAS': 'MYS',  # Malaysia
    'MAW': 'MWI',  # Malawi
    'MDA': 'MDA',  # Moldova
    'MDV': 'MDV',  # Maldives
    'MEX': 'MEX',  # Mexico
    'MGL': 'MNG',  # Mongolia
    'MHL': 'MHL',  # Marshall Islands
    'MKD': 'MKD',  # North Macedonia
    'MLI': 'MLI',  # Mali
    'MLT': 'MLT',  # Malta
    'MNE': 'MNE',  # Montenegro
    'MON': 'MCO',  # Monaco
    'MOZ': 'MOZ',  # Mozambique
    'MRI': 'MUS',  # Mauritius
    'MTN': 'MRT',  # Mauritania
    'MYA': 'MMR',  # Myanmar
    'NAM': 'NAM',  # Namibia
    'NCA': 'NIC',  # Nicaragua
    'NED': 'NLD',  # Netherlands
    'NEP': 'NPL',  # Nepal
    'NGR': 'NGA',  # Nigeria
    'NIG': 'NER',  # Niger
    'NOR': 'NOR',  # Norway
    'NRU': 'NRU',  # Nauru
    'NZL': 'NZL',  # New Zealand
    'OMA': 'OMN',  # Oman
    'PAK': 'PAK',  # Pakistan
    'PAN': 'PAN',  # Panama
    'PAR': 'PRY',  # Paraguay
    'PER': 'PER',  # Peru
    'PHI': 'PHL',  # Philippines
    'PLE': 'PSE',  # Palestine
    'PLW': 'PLW',  # Palau
    'PNG': 'PNG',  # Papua New Guinea
    'POL': 'POL',  # Poland
    'POR': 'PRT',  # Portugal
    'PRK': 'PRK',  # North Korea
    'PUR': 'PRI',  # Puerto Rico
    'QAT': 'QAT',  # Qatar
    'ROU': 'ROU',  # Romania
    'RSA': 'ZAF',  # South Africa
    'RUS': 'RUS',  # Russia
    'RWA': 'RWA',  # Rwanda
    'SAM': 'WSM',  # Samoa
    'SEN': 'SEN',  # Senegal
    'SEY': 'SYC',  # Seychelles
    'SGP': 'SGP',  # Singapore
    'SKN': 'KNA',  # Saint Kitts and Nevis
    'SLE': 'SLE',  # Sierra Leone
    'SLO': 'SVN',  # Slovenia
    'SMR': 'SMR',  # San Marino
    'SOL': 'SLB',  # Solomon Islands
    'SOM': 'SOM',  # Somalia
    'SRB': 'SRB',  # Serbia
    'SRI': 'LKA',  # Sri Lanka
    'SSD': 'SSD',  # South Sudan
    'STP': 'STP',  # São Tomé and Príncipe
    'SUD': 'SDN',  # Sudan
    'SUI': 'CHE',  # Switzerland - IOC uses French abbreviation
    'SUR': 'SUR',  # Suriname
    'SVK': 'SVK',  # Slovakia
    'SWE': 'SWE',  # Sweden
    'SWZ': 'SWZ',  # Eswatini
    'SYR': 'SYR',  # Syria
    'TAN': 'TZA',  # Tanzania
    'TGA': 'TON',  # Tonga
    'THA': 'THA',  # Thailand
    'TJK': 'TJK',  # Tajikistan
    'TKM': 'TKM',  # Turkmenistan
    'TLS': 'TLS',  # Timor-Leste
    'TOG': 'TGO',  # Togo
    'TPE': 'TWN',  # Chinese Taipei (Taiwan)
    'TTO': 'TTO',  # Trinidad and Tobago
    'TUN': 'TUN',  # Tunisia
    'TUR': 'TUR',  # Turkey
    'TUV': 'TUV',  # Tuvalu
    'UAE': 'ARE',  # United Arab Emirates
    'UGA': 'UGA',  # Uganda
    'UKR': 'UKR',  # Ukraine
    'URU': 'URY',  # Uruguay
    'USA': 'USA',  # United States
    'UZB': 'UZB',  # Uzbekistan
    'VAN': 'VUT',  # Vanuatu
    'VEN': 'VEN',  # Venezuela
    'VIE': 'VNM',  # Vietnam
    'VIN': 'VCT',  # Saint Vincent and the Grenadines
    'YEM': 'YEM',  # Yemen
    'ZAM': 'ZMB',  # Zambia
    'ZIM': 'ZWE',  # Zimbabwe
    
    # Historical / Special codes for Olympic teams that aren't countries
    'EOR': 'EOR', # Refugee Olympic Team - No ISO, usually handled specially or mapped to something else?
    'ROC': 'RUS', # Russian Olympic Committee -> Russia
    'AIN': 'AIN', # Individual Neutral Athletes -> No ISO
}


def get_iso_code(ioc_code):
    """
    Convert an IOC country code to an ISO 3166-1 alpha-3 code.
    
    This function is used to prepare data for Plotly choropleth maps,
    which require ISO codes for country identification.
    
    Args:
        ioc_code: The IOC country code (e.g., 'GER', 'SUI', 'USA')
    
    Returns:
        The corresponding ISO code (e.g., 'DEU', 'CHE', 'USA'),
        or the original code if no mapping exists.
    
    Example:
        >>> get_iso_code('GER')
        'DEU'
        >>> get_iso_code('USA')
        'USA'
    """
    # .get() looks up the key in the dictionary
    # The second argument is the default value if the key isn't found
    # We return the original code as a fallback for unmapped codes
    return IOC_TO_ISO.get(ioc_code, ioc_code)
