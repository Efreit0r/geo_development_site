"""Создаёт tl_2015_us_cbsa.shp — упрощённые границы метрополитенских
статистических ареалов (CBSA) Калифорнии в NAD83, как у TIGER/Line.

Нужен скрипту findNearbyParks.py (поле NAME + полигоны).
"""

import os
from osgeo import ogr, osr

# (NAME, NAMELSAD, GEOID, прямоугольник lon_min, lon_max, lat_min, lat_max)
CBSA = [
    ("Los Angeles-Long Beach-Anaheim, CA", "Los Angeles-Long Beach-Anaheim, CA Metro Area",
     "31080", -119.00, -117.60, 33.50, 34.40),
    ("San Francisco-Oakland-Hayward, CA", "San Francisco-Oakland-Hayward, CA Metro Area",
     "41860", -122.60, -121.95, 37.20, 38.10),
    ("San Diego-Carlsbad, CA", "San Diego-Carlsbad, CA Metro Area",
     "41740", -117.40, -116.60, 32.50, 33.30),
    ("Sacramento--Roseville--Arden-Arcade, CA", "Sacramento--Roseville--Arden-Arcade, CA Metro Area",
     "40900", -121.70, -120.90, 38.30, 38.90),
    ("San Jose-Sunnyvale-Santa Clara, CA", "San Jose-Sunnyvale-Santa Clara, CA Metro Area",
     "41940", -121.95, -121.35, 37.00, 37.50),
    ("Fresno, CA", "Fresno, CA Metro Area",
     "23420", -120.10, -119.40, 36.50, 37.00),
    ("Bakersfield, CA", "Bakersfield, CA Metro Area",
     "12540", -119.50, -118.60, 35.00, 35.60),
    ("Chico, CA", "Chico, CA Metro Area",
     "17020", -121.95, -121.60, 39.60, 39.90),
]

sr = osr.SpatialReference()
sr.ImportFromEPSG(4269)                 # NAD83, как в TIGER/Line
sr.SetAxisMappingStrategy(osr.OAMS_TRADITIONAL_GIS_ORDER)  # x=lon, y=lat

driver = ogr.GetDriverByName("ESRI Shapefile")
path = os.path.join(os.getcwd(), "tl_2015_us_cbsa.shp")
if os.path.exists(path):
    driver.DeleteDataSource(path)

ds = driver.CreateDataSource(path)
layer = ds.CreateLayer("tl_2015_us_cbsa", sr, ogr.wkbPolygon)
for name in ("STATEFP", "GEOID", "NAME", "NAMELSAD", "ALAND"):
    if name == "ALAND":
        layer.CreateField(ogr.FieldDefn(name, ogr.OFTInteger64))
    else:
        layer.CreateField(ogr.FieldDefn(name, ogr.OFTString))


def block(ring_pts):
    """Полигон из списка точек с лёгкой «ступенчатостью» по краям."""
    ring = ogr.Geometry(ogr.wkbLinearRing)
    for x, y in ring_pts:
        ring.AddPoint(x, y)
    ring.AddPoint(*ring_pts[0])
    poly = ogr.Geometry(ogr.wkbPolygon)
    poly.AddGeometry(ring)
    return poly


for name, namelsad, geoid, lon0, lon1, lat0, lat1 in CBSA:
    mx, my = (lon0 + lon1) / 2.0, (lat0 + lat1) / 2.0
    # Похожие на объединение округов контуры: углы + ступеньки на серединах сторон.
    pts = [
        (lon0, lat0),
        (mx - (mx - lon0) * 0.1, lat0),
        (mx - (mx - lon0) * 0.1, lat0 + (lat1 - lat0) * 0.08),
        (mx + (lon1 - mx) * 0.15, lat0 + (lat1 - lat0) * 0.08),
        (mx + (lon1 - mx) * 0.15, lat0),
        (lon1, lat0),
        (lon1, my - (my - lat0) * 0.1),
        (lon1 - (lon1 - mx) * 0.12, my - (my - lat0) * 0.1),
        (lon1 - (lon1 - mx) * 0.12, my + (lat1 - my) * 0.12),
        (lon1, my + (lat1 - my) * 0.12),
        (lon1, lat1),
        (mx + (lon1 - mx) * 0.2, lat1),
        (mx + (lon1 - mx) * 0.2, lat1 - (lat1 - lat0) * 0.1),
        (mx - (mx - lon0) * 0.2, lat1 - (lat1 - lat0) * 0.1),
        (mx - (mx - lon0) * 0.2, lat1),
        (lon0, lat1),
        (lon0, my + (lat1 - my) * 0.15),
        (lon0 + (mx - lon0) * 0.1, my + (lat1 - my) * 0.15),
        (lon0 + (mx - lon0) * 0.1, my - (my - lat0) * 0.15),
        (lon0, my - (my - lat0) * 0.15),
    ]

    feature = ogr.Feature(layer.GetLayerDefn())
    feature.SetField("STATEFP", "06")
    feature.SetField("GEOID", geoid)
    feature.SetField("NAME", name)
    feature.SetField("NAMELSAD", namelsad)
    feature.SetField("ALAND", 0)
    feature.SetGeometry(block(pts))
    layer.CreateFeature(feature)

ds = None
print("Создан:", path, "— ареалов:", len(CBSA))
