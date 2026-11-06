# changeProjection.py

import os, os.path, shutil
from osgeo import ogr
from osgeo import osr
from osgeo import gdal

# Define the source and destination projections, and a
# transformation object to convert from one to the other.

srcProjection = osr.SpatialReference()
srcProjection.SetUTM(17)

dstProjection = osr.SpatialReference()
dstProjection.SetWellKnownGeogCS('WGS84') # Lat/long.
# GDAL 3 по умолчанию отдаёт EPSG:4326 в порядке (lat, lon); shapefile ждёт (lon, lat).
dstProjection.SetAxisMappingStrategy(osr.OAMS_TRADITIONAL_GIS_ORDER)

transform = osr.CoordinateTransformation(srcProjection,
                                         dstProjection)

# Open the source shapefile.

srcFile = ogr.Open("miami/miami.shp")
srcLayer = srcFile.GetLayer(0)

print("Источник: miami/miami.shp (UTM zone 17N)")
print("Объектов в источнике:", srcLayer.GetFeatureCount())

# Create the dest shapefile, and give it the new projection.

if os.path.exists("miami-reprojected"):
    shutil.rmtree("miami-reprojected")
os.mkdir("miami-reprojected")

driver = ogr.GetDriverByName("ESRI Shapefile")
dstPath = os.path.join("miami-reprojected", "miami.shp")
dstFile = driver.CreateDataSource(dstPath)
dstLayer = dstFile.CreateLayer("layer", dstProjection)

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

print("Целевая проекция: WGS84 (EPSG:4326)")
print("Записано:", dstPath, "— объектов:", written)
if skipped:
    print("Пропущено объектов без геометрии:", skipped)

