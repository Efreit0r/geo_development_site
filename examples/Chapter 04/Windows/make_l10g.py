"""Создаёт растр l10g — GeoTIFF с одним каналом Int16 (модель рельефа),
как в книжном примере: gdal.Open("l10g").

Область покрывает окно из histogram.py (165..179 в.д., -48..-33 ю.ш.)
с запасом по краям, чтобы чтение на границе не выходило за растр.
Разрешение 30 угловых секунд (1/120 градуса), как у GLOBE l10g.
"""

import numpy as np
from osgeo import gdal, osr

RES = 1.0 / 120.0          # 30 угловых секунд
WEST, EAST = 164.5, 180.0  # запас по 0.5° с каждой стороны
NORTH, SOUTH = -32.5, -48.5

width = int(round((EAST - WEST) / RES))
height = int(round((NORTH - SOUTH) / RES))

lon = np.linspace(WEST + RES / 2, EAST - RES / 2, width)
lat = np.linspace(NORTH - RES / 2, SOUTH + RES / 2, height)
lon2d, lat2d = np.meshgrid(lon, lat)

# Береговая линия: суша восточнее плавно изгибающейся линии.
coast = 171.0 + 1.5 * np.sin(np.radians(lat2d * 30)) + 0.8 * np.sin(np.radians(lat2d * 7))
is_land = lon2d > coast

# Суша: хребет + крупные и мелкие неровности.
ridge = (900 * np.exp(-((lon2d - 176.0) ** 2) / 6.0)
         * np.exp(-((lat2d + 40.0) ** 2) / 40.0))
land = (250 + ridge
        + 300 * np.sin(np.radians(lon2d * 34)) * np.cos(np.radians(lat2d * 46))
        + 150 * np.sin(np.radians(lon2d * 120) + 1.3 * np.radians(lat2d * 90))
        + 60 * np.sin(np.radians(lon2d * 400)) * np.cos(np.radians(lat2d * 380)))

# Океан: шельф у берега и глубина на западе.
sea = -(250 + 2600 * np.exp(-((lon2d - 166.0) ** 2) / 8.0)
        + 120 * np.sin(np.radians(lat2d * 60)))

elevation = np.where(is_land, land, sea)
elevation = np.clip(elevation, -4000, 3000)
# Округление до 100 м: гистограмма получается читаемой (десятки строк).
elevation = np.round(elevation / 100.0) * 100.0
elevation = elevation.astype(np.int16)

driver = gdal.GetDriverByName("GTiff")
dataset = driver.Create("l10g", width, height, 1, gdal.GDT_Int16,
                        options=["COMPRESS=DEFLATE", "TILED=YES"])
dataset.SetGeoTransform((WEST, RES, 0.0, NORTH, 0.0, -RES))

sr = osr.SpatialReference()
sr.ImportFromEPSG(4326)
sr.SetAxisMappingStrategy(osr.OAMS_TRADITIONAL_GIS_ORDER)
dataset.SetProjection(sr.ExportToWkt())

band = dataset.GetRasterBand(1)
band.SetNoDataValue(-32768)
band.WriteArray(elevation)
band.SetDescription("Elevation (m), synthetic DEM")
dataset.FlushCache()
dataset = None

print("Создан: l10g — %d x %d, Int16" % (width, height))
print("Экстент: lon %.1f..%.1f, lat %.1f..%.1f" % (WEST, EAST, SOUTH, NORTH))
print("Значения: %d..%d м, различных высот: %d"
      % (elevation.min(), elevation.max(), len(np.unique(elevation))))
