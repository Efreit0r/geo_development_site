"""Создаёт CA_Features_2024.txt — выгрузку в формате GNIS (USGS)
для Калифорнии: 20 столбцов через "|", как в настоящем CA_Features_*.txt.

Нужна скриптам findShoshone.py и findNearbyParks.py.
"""

import os

# (имя, класс, округ, широта, долгота, высота в метрах)
FEATURES = [
    # --- населённые пункты ---
    ("Shoshone", "Populated Place", "Inyo", 35.97300, -116.27110, 483),
    ("Los Angeles", "Populated Place", "Los Angeles", 34.05220, -118.24370, 87),
    ("San Francisco", "Populated Place", "San Francisco", 37.77490, -122.41940, 16),
    ("San Diego", "Populated Place", "San Diego", 32.71570, -117.16110, 20),
    ("Sacramento", "Populated Place", "Sacramento", 38.58160, -121.49440, 9),
    ("Fresno", "Populated Place", "Fresno", 36.73780, -119.78710, 94),
    ("Bakersfield", "Populated Place", "Kern", 35.37330, -119.01870, 123),
    ("Long Beach", "Populated Place", "Los Angeles", 33.77010, -118.19370, 16),
    ("Pasadena", "Populated Place", "Los Angeles", 34.14780, -118.14450, 263),
    ("Santa Monica", "Populated Place", "Los Angeles", 34.01950, -118.49120, 32),
    ("Oakland", "Populated Place", "Alameda", 37.80440, -122.27120, 13),
    ("Berkeley", "Populated Place", "Alameda", 37.87150, -122.27300, 52),
    ("San Jose", "Populated Place", "Santa Clara", 37.33820, -121.88630, 25),
    ("Stockton", "Populated Place", "San Joaquin", 37.95770, -121.29080, 4),
    ("Modesto", "Populated Place", "Stanislaus", 37.63910, -120.99690, 27),
    ("Santa Barbara", "Populated Place", "Santa Barbara", 34.42080, -119.69820, 15),
    ("Ventura", "Populated Place", "Ventura", 34.27460, -119.22900, 11),
    ("Monterey", "Populated Place", "Monterey", 36.60020, -121.89470, 8),
    ("Santa Cruz", "Populated Place", "Santa Cruz", 36.97410, -122.03080, 11),
    ("Eureka", "Populated Place", "Humboldt", 40.80210, -124.16370, 12),
    ("Redding", "Populated Place", "Shasta", 40.58650, -122.39170, 172),
    ("Chico", "Populated Place", "Butte", 39.72850, -121.83750, 60),
    ("Susanville", "Populated Place", "Lassen", 40.41630, -120.65300, 1276),
    ("Truckee", "Populated Place", "Nevada", 39.32800, -120.18330, 1773),
    ("South Lake Tahoe", "Populated Place", "El Dorado", 38.93990, -119.97720, 1901),
    ("Mammoth Lakes", "Populated Place", "Mono", 37.64850, -118.97210, 2402),
    ("Bishop", "Populated Place", "Inyo", 37.36350, -118.39510, 1264),
    ("Lone Pine", "Populated Place", "Inyo", 36.60630, -118.06450, 1136),
    ("Independence", "Populated Place", "Inyo", 36.80270, -118.20010, 1193),
    ("Ridgecrest", "Populated Place", "Kern", 35.62250, -117.67090, 698),
    ("Barstow", "Populated Place", "San Bernardino", 34.89580, -117.01730, 663),
    ("Baker", "Populated Place", "San Bernardino", 35.26550, -116.07470, 283),
    ("Needles", "Populated Place", "San Bernardino", 34.84810, -114.61410, 150),
    ("Palm Springs", "Populated Place", "Riverside", 33.83030, -116.54530, 146),
    ("Riverside", "Populated Place", "Riverside", 33.95330, -117.39620, 262),
    ("San Bernardino", "Populated Place", "San Bernardino", 34.10830, -117.28980, 321),
    ("Death Valley Junction", "Populated Place", "Inyo", 36.30270, -116.41470, 610),
    ("Tecopa", "Populated Place", "Inyo", 35.84830, -116.22640, 408),

    # --- парки (нужны findNearbyParks.py) ---
    ("Griffith Park", "Park", "Los Angeles", 34.13410, -118.30000, 384),
    ("Balboa Park", "Park", "San Diego", 32.73410, -117.14460, 72),
    ("Golden Gate Park", "Park", "San Francisco", 37.76940, -122.48620, 40),
    ("Alum Rock Park", "Park", "Santa Clara", 37.39330, -121.82000, 200),
    ("Bidwell Park", "Park", "Butte", 39.75000, -121.80000, 80),
    ("Joshua Tree National Park", "Park", "San Bernardino", 33.87340, -115.90100, 1280),
    ("Yosemite National Park", "Park", "Mariposa", 37.74560, -119.59360, 1200),
    ("Sequoia National Park", "Park", "Tulare", 36.48640, -118.56580, 1400),
    ("Death Valley National Park", "Park", "Inyo", 36.50540, -117.07940, 60),
    ("Humboldt Redwoods State Park", "Park", "Humboldt", 40.33000, -123.90000, 120),

    # --- прочие объекты ---
    ("Los Angeles River", "Stream", "Los Angeles", 34.05000, -118.24000, 90),
    ("Sacramento River", "Stream", "Sacramento", 38.55000, -121.50000, 6),
    ("Mount Whitney", "Summit", "Inyo", 36.57850, -118.29230, 4421),
    ("Mount Shasta", "Summit", "Siskiyou", 41.40920, -122.19430, 4322),
    ("Death Valley", "Valley", "Inyo", 36.23970, -116.77010, -86),
    ("Coachella Valley", "Valley", "Riverside", 33.70000, -116.30000, 30),
    ("Lake Tahoe", "Lake", "El Dorado", 39.09680, -120.03240, 1897),
    ("Lake Merritt", "Lake", "Alameda", 37.80600, -122.25700, 4),
    ("Salton Sea", "Lake", "Imperial", 33.32000, -115.83000, -71),
    ("San Francisco Bay", "Bay", "San Francisco", 37.78000, -122.36000, 0),
    ("Monterey Bay", "Bay", "Monterey", 36.80000, -121.95000, 0),
    ("Alcatraz Island", "Island", "San Francisco", 37.82670, -122.42300, 41),
    ("Mojave Desert", "Plain", "San Bernardino", 35.00000, -116.00000, 900),
    ("Los Angeles International Airport", "Airport", "Los Angeles", 33.94250, -118.40810, 38),
]

# FIPS округов Калифорнии (для столбца COUNTY_NUMERIC).
FIPS = {
    "Alameda": "001", "Butte": "007", "El Dorado": "017", "Fresno": "019",
    "Humboldt": "023", "Imperial": "025", "Inyo": "027", "Kern": "029",
    "Lassen": "035", "Los Angeles": "037", "Mariposa": "043",
    "Monterey": "053", "Nevada": "057", "Riverside": "065",
    "Sacramento": "067", "San Bernardino": "071", "San Diego": "073",
    "San Francisco": "075", "San Joaquin": "077", "Santa Barbara": "083",
    "Santa Clara": "085", "Santa Cruz": "087", "Shasta": "089",
    "Siskiyou": "093", "Stanislaus": "099", "Tulare": "107", "Ventura": "111",
}


def dms(value, lat):
    """Градусы-минуты-секунды в стиле GNIS: 355823N / 1161617W."""
    hemi = ("N" if value >= 0 else "S") if lat else ("E" if value >= 0 else "W")
    total = int(round(abs(value) * 3600))
    deg, rem = divmod(total, 3600)
    minutes, seconds = divmod(rem, 60)
    width = 2 if lat else 3
    return "%0*d%02d%02d%s" % (width, deg, minutes, seconds, hemi)


rows = []
for feature_id, (name, cls, county, lat, lon, elev_m) in enumerate(FEATURES, start=1):
    rows.append("|".join([
        str(feature_id),                       # FEATURE_ID
        name,                                  # FEATURE_NAME
        cls,                                   # FEATURE_CLASS
        "CA",                                  # STATE_ALPHA
        "06",                                  # STATE_NUMERIC
        county,                                # COUNTY_NAME
        FIPS.get(county, "999"),               # COUNTY_NUMERIC
        dms(lat, True), dms(lon, False),       # PRIMARY_LAT_DMS, PRIM_LONG_DMS
        "%.6f" % lat, "%.6f" % lon,            # PRIM_LAT_DEC, PRIM_LONG_DEC
        dms(lat, True), dms(lon, False),       # SOURCE_* (упрощённо = PRIMARY)
        "%.6f" % lat, "%.6f" % lon,
        str(elev_m),                           # ELEV_IN_M
        str(int(round(elev_m * 3.28084))),     # ELEV_IN_FT
        name,                                  # MAP_NAME
        "1981-01-19", "2024-01-01",            # DATE_CREATED, DATE_EDITED
    ]))

path = os.path.join(os.getcwd(), "CA_Features_2024.txt")
with open(path, "w", encoding="utf-8", newline="\n") as f:
    f.write("\n".join(rows) + "\n")

print("Создан:", path, "— записей:", len(rows))
