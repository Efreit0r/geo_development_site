# changeDatum.py

import os, os.path, shutil
from osgeo import ogr
from osgeo import osr
from osgeo import gdal

# Define the source and destination datums, and a
# transformation object to convert from one to the other.

srcDatum = osr.SpatialReference()
srcDatum.SetWellKnownGeogCS('NAD27')
srcDatum.SetAxisMappingStrategy(osr.OAMS_TRADITIONAL_GIS_ORDER)

dstDatum = osr.SpatialReference()
dstDatum.SetWellKnownGeogCS('WGS84')
# GDAL 3 отдаёт EPSG:4326 в порядке (lat, lon); shapefile ждёт (lon, lat).
dstDatum.SetAxisMappingStrategy(osr.OAMS_TRADITIONAL_GIS_ORDER)

transform = osr.CoordinateTransformation(srcDatum, dstDatum)

# Open the source shapefile.

srcFile = ogr.Open("roads/roads.shp")
srcLayer = srcFile.GetLayer(0)

print("Источник: roads/roads.shp (NAD27)")
print("Объектов в источнике:", srcLayer.GetFeatureCount())

# Create the dest shapefile, and give it the new projection.

if os.path.exists("roads-reprojected"):
    shutil.rmtree("roads-reprojected")
os.mkdir("roads-reprojected")

driver = ogr.GetDriverByName("ESRI Shapefile")
dstPath = os.path.join("roads-reprojected", "roads.shp")
dstFile = driver.CreateDataSource(dstPath)
dstLayer = dstFile.CreateLayer("layer", dstDatum)

# Reproject each feature in turn.

written = 0
skipped = 0

for i in range(srcLayer.GetFeatureCount()):
    feature = srcLayer.GetFeature(i)
    geometry = feature.GetGeometryRef()

    if geometry is None:
        skipped += 1
        continue

    newGeometry = geometry.Clone()
    newGeometry.Transform(transform)

    feature = ogr.Feature(dstLayer.GetLayerDefn())
    feature.SetGeometry(newGeometry)
    dstLayer.CreateFeature(feature)
    written += 1

dstFile = None   # закрыть файл, чтобы данные точно попали на диск

print("Целевой датум: WGS84 (EPSG:4326)")
print("Записано:", dstPath, "— объектов:", written)
if skipped:
    print("Пропущено объектов без геометрии:", skipped)

