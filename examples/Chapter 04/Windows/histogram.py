# histogram.py

import sys, struct
from osgeo import gdal
from osgeo import gdalconst

minLat  = -48
maxLat  = -33
minLong = 165
maxLong = 179

dataset = gdal.Open("l10g")
band = dataset.GetRasterBand(1)

t = dataset.GetGeoTransform()

# GDAL 3.x возвращает сразу 6 коэффициентов обратного преобразования,
# старые версии — пару (success, coefficients).
result = gdal.InvGeoTransform(t)
if isinstance(result, (tuple, list)) and len(result) == 2:
    success, tInverse = result
else:
    tInverse = result
    success = tInverse is not None
if not success:
    print("Failed!")
    sys.exit(1)

x1,y1 = gdal.ApplyGeoTransform(tInverse, minLong, minLat)
x2,y2 = gdal.ApplyGeoTransform(tInverse, maxLong, maxLat)

minX = int(min(x1, x2))
maxX = int(max(x1, x2))
minY = int(min(y1, y2))
maxY = int(max(y1, y2))

width = (maxX - minX) + 1
fmt = "<" + ("h" * width)

histogram = {} # Maps elevation to number of occurrences.

for y in range(minY, maxY+1):
    scanline = band.ReadRaster(minX, y, width, 1,
                               width, 1,
                               gdalconst.GDT_Int16)
    values = struct.unpack(fmt, scanline)

    for value in values:
        try:
            histogram[value] += 1
        except KeyError:
            histogram[value] = 1

for height in sorted(histogram.keys()):
    print(height, histogram[height])

