"""Создаёт miami/miami.shp — небольшой векторный слой в UTM 17N (WGS84),
который ожидает changeProjection.py на входе."""

import os
from osgeo import ogr, osr

# Полигоны в градусах (lon, lat) — районы Майами и окрестности.
FEATURES = [
    ("Downtown Miami", "district", [(-80.200, 25.755), (-80.180, 25.755),
                                    (-80.178, 25.778), (-80.199, 25.780),
                                    (-80.200, 25.755)]),
    ("Miami Beach", "city", [(-80.142, 25.790), (-80.128, 25.790),
                             (-80.118, 25.870), (-80.133, 25.872),
                             (-80.142, 25.790)]),
    ("Coconut Grove", "district", [(-80.252, 25.710), (-80.222, 25.712),
                                   (-80.220, 25.742), (-80.250, 25.740),
                                   (-80.252, 25.710)]),
    ("Little Havana", "district", [(-80.230, 25.762), (-80.203, 25.762),
                                   (-80.202, 25.778), (-80.229, 25.778),
                                   (-80.230, 25.762)]),
    ("Port of Miami", "port", [(-80.176, 25.764), (-80.160, 25.764),
                               (-80.158, 25.782), (-80.175, 25.782),
                               (-80.176, 25.764)]),
]

srcSR = osr.SpatialReference()
srcSR.ImportFromEPSG(4326)              # lon/lat WGS84
srcSR.SetAxisMappingStrategy(osr.OAMS_TRADITIONAL_GIS_ORDER)  # x=lon, y=lat
dstSR = osr.SpatialReference()
dstSR.SetUTM(17)                        # UTM zone 17N — то же, что в скрипте
dstSR.SetAxisMappingStrategy(osr.OAMS_TRADITIONAL_GIS_ORDER)
transform = osr.CoordinateTransformation(srcSR, dstSR)

out_dir = os.path.join(os.getcwd(), "miami")
os.makedirs(out_dir, exist_ok=True)

driver = ogr.GetDriverByName("ESRI Shapefile")
path = os.path.join(out_dir, "miami.shp")
if os.path.exists(path):
    driver.DeleteDataSource(path)

ds = driver.CreateDataSource(path)
layer = ds.CreateLayer("miami", dstSR, ogr.wkbPolygon)

for name, kind in (("NAME", ogr.OFTString), ("TYPE", ogr.OFTString)):
    layer.CreateField(ogr.FieldDefn(name, kind))

for title, kind, ring in FEATURES:
    geom = ogr.Geometry(ogr.wkbPolygon)
    outer = ogr.Geometry(ogr.wkbLinearRing)
    for x, y in ring:
        outer.AddPoint(x, y)
    geom.AddGeometry(outer)
    geom.Transform(transform)           # -> UTM 17N, метры

    feature = ogr.Feature(layer.GetLayerDefn())
    feature.SetField("NAME", title)
    feature.SetField("TYPE", kind)
    feature.SetGeometry(geom)
    layer.CreateFeature(feature)

ds = None
print("Создан:", path)
