# histogram_chart.py — гистограмма высот растра в виде полос в терминале.
#
# Самостоятельный скрипт: книжный histogram.py не трогает и ничего не требует,
# кроме растра (по умолчанию "l10g"), лежащего в текущем каталоге.
#
# Примеры:
#   python3 histogram_chart.py
#   python3 histogram_chart.py --log                 # логарифмический масштаб
#   python3 histogram_chart.py --bins 200            # шаг 200 м вместо родного
#   python3 histogram_chart.py --width 70 --file l10g

import argparse
import math

import numpy as np
from osgeo import gdal

FULL = "\u2588"                 # █
PARTS = " \u258f\u258e\u258d\u258c\u258b\u258a\u2589"   # ▏▎▍▌▋▊▉


def inverse_geotransform(gt):
    """GDAL 3.x отдаёт 6 коэффициентов, старые версии — (success, coefficients)."""
    result = gdal.InvGeoTransform(gt)
    if isinstance(result, (tuple, list)) and len(result) == 2:
        success, inverse = result
    else:
        inverse, success = result, result is not None
    return inverse if success else None


def draw_bar(value, maximum, width, log_scale):
    if maximum <= 0 or value <= 0:
        return ""
    if log_scale:
        fraction = math.log1p(value) / math.log1p(maximum)
    else:
        fraction = value / maximum
    cells = fraction * width
    full = int(cells)
    partial = int((cells - full) * 8)
    if full >= width:
        return FULL * width
    return FULL * full + (PARTS[partial] if partial else "")


def main():
    parser = argparse.ArgumentParser(
        description="Гистограмма высот растра полосами в терминале")
    parser.add_argument("--file", default="l10g", help="растр (по умолчанию l10g)")
    parser.add_argument("--width", type=int, default=50, help="длина полосы в знакоместах")
    parser.add_argument("--bins", type=int, default=0,
                        help="шаг группировки высот, м (0 — как в растре)")
    parser.add_argument("--log", action="store_true", help="логарифмический масштаб полос")
    parser.add_argument("--minLat", type=float, default=-48.0)
    parser.add_argument("--maxLat", type=float, default=-33.0)
    parser.add_argument("--minLong", type=float, default=165.0)
    parser.add_argument("--maxLong", type=float, default=179.0)
    args = parser.parse_args()

    dataset = gdal.Open(args.file)
    if dataset is None:
        raise SystemExit("Не удалось открыть растр: %s" % args.file)
    band = dataset.GetRasterBand(1)

    inverse = inverse_geotransform(dataset.GetGeoTransform())
    if inverse is None:
        raise SystemExit("Не удалось обратить геотрансформ растра.")

    x1, y1 = gdal.ApplyGeoTransform(inverse, args.minLong, args.minLat)
    x2, y2 = gdal.ApplyGeoTransform(inverse, args.maxLong, args.maxLat)
    minX, maxX = int(min(x1, x2)), int(max(x1, x2))
    minY, maxY = int(min(y1, y2)), int(max(y1, y2))
    width, height = maxX - minX + 1, maxY - minY + 1

    values = band.ReadAsArray(minX, minY, width, height)
    if values is None:
        raise SystemExit("Не удалось прочитать окно растра.")
    values = values.astype(np.int64).ravel()
    raw_min, raw_max = int(values.min()), int(values.max())

    if args.bins and args.bins > 0:
        values = np.floor_divide(values, args.bins) * args.bins

    levels, counts = np.unique(values, return_counts=True)
    maximum = int(counts.max())
    total = int(counts.sum())

    cells = len(values)
    average = float(values.mean())
    median = int(levels[np.searchsorted(np.cumsum(counts), total / 2.0)])

    print("Растр: %s (%d x %d, %s)" % (args.file, dataset.RasterXSize,
                                       dataset.RasterYSize,
                                       gdal.GetDataTypeName(band.DataType)))
    print("Окно: lon %.1f..%.1f, lat %.1f..%.1f — %d x %d пикселей, %d значений"
          % (args.minLong, args.maxLong, args.minLat, args.maxLat, width, height, total))
    if args.bins:
        print("Интервал группировки: %d м" % args.bins)
    print("Масштаб полос: %s" % ("логарифмический" if args.log else "линейный"))
    print()

    label_width = max(len(str(int(level))) for level in levels) + 1
    for level, count in zip(levels, counts):
        bar = draw_bar(int(count), maximum, args.width, args.log).ljust(args.width + 1)
        print("%*d \u2502%s\u2502 %8d %5.1f%%"
              % (label_width, int(level), bar, count, 100.0 * count / total))

    print()
    print("Всего значений: %d" % total)
    if args.bins:
        print("Уровни (левая граница интервала): %d..%d м, интервалов: %d"
              % (int(levels.min()), int(levels.max()), len(levels)))
        print("Фактические высоты: %d..%d м" % (raw_min, raw_max))
    else:
        print("Высот: %d..%d м, различных уровней: %d"
              % (int(levels.min()), int(levels.max()), len(levels)))
    print("Средняя высота: %.0f м, медиана: %d м" % (average, median))
    print("Самая частая высота: %d м (%d значений, %.1f%%)"
          % (int(levels[counts.argmax()]), maximum, 100.0 * maximum / total))
    print("Клеток (учитывая все окно): %d" % cells)


if __name__ == "__main__":
    main()
