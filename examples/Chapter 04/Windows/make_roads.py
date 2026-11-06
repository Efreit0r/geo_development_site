"""Создаёт roads/roads.shp — линейный слой улиц в NAD27 (EPSG:4267),
который ожидает changeDatum.py на входе."""

import os
from osgeo import ogr, osr

# Улицы в градусах (lon, lat) — Майами.
ROADS = [
    ("Biscayne Blvd", "primary", [(-80.1918, 25.7550), (-80.1910, 25.7700),
                                  (-80.1895, 25.7850)]),
    ("Flagler St", "secondary", [(-80.2050, 25.7740), (-80.1900, 25.7742),
                                 (-80.1780, 25.7745)]),
    ("SE 2nd Ave", "secondary", [(-80.1900, 25.7600), (-80.1898, 25.7742)]),
    ("Brickell Ave", "primary", [(-80.1918, 25.7550), (-80.1920, 25.7450),
                                 (-80.1930, 25.7350)]),
    ("Ocean Drive", "secondary", [(-80.1300, 25.7800), (-80.1295, 25.8000),
                                  (-80.1280, 25.8150)]),
    ("Calle Ocho", "secondary", [(-80.2250, 25.7650), (-80.2050, 25.7652),
                                 (-80.1900, 25.7655)]),
]

srcSR = osr.SpatialReference()
srcSR.ImportFromEPSG(4267)              # NAD27
srcSR.SetAxisMappingStrategy(osr.OAMS_TRADITIONAL_GIS_ORDER)  # x=lon, y=lat

out_dir = os.path.join(os.getcwd(), "roads")
os.makedirs(out_dir, exist_ok=True)

driver = ogr.GetDriverByName("ESRI Shapefile")
path = os.path.join(out_dir, "roads.shp")
if os.path.exists(path):
    driver.DeleteDataSource(path)

ds = driver.CreateDataSource(path)
layer = ds.CreateLayer("roads", srcSR, ogr.wkbLineString)
layer.CreateField(ogr.FieldDefn("NAME", ogr.OFTString))
layer.CreateField(ogr.FieldDefn("TYPE", ogr.OFTString))

for name, kind, points in ROADS:
    line = ogr.Geometry(ogr.wkbLineString)
    for x, y in points:
        line.AddPoint(x, y)

    feature = ogr.Feature(layer.GetLayerDefn())
    feature.SetField("NAME", name)
    feature.SetField("TYPE", kind)
    feature.SetGeometry(line)
    layer.CreateFeature(feature)

ds = None
print("Создан:", path)
