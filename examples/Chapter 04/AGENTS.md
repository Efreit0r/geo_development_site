# AGENTS.md — Chapter 04

Archive of book exercises, not a buildable project: no git, tests, linter, or dependency manifest. "Verify" means running one script. Archive-wide notes live in `../../../AGENTS.md`.

## What's here

- Nine standalone scripts in `Windows/` (the only subdirectory): OGR/OSR reprojection, Shapely geometry ops, `pyproj` geodesic math, and one GDAL raster histogram.
- `geo_operations.md` — self-contained Slidev deck (Russian, beginner-level) walking through these scripts. Run it from `../../../Geo_development` (the only place `@slidev/cli` is installed; needs Node 20+): `./node_modules/.bin/slidev geo_operations.md`, adding the path to this file. Inline SVG/emoji only, so keep new slides free of external images. Building/exporting drops a throwaway `node_modules/.slidev/` cache next to the deck — delete it afterwards; there is no `.gitignore` here.
- All scripts open data by bare relative path, so `cd` into a directory holding the data before running. Do not edit files in place to add paths.
- System `python3` (3.12) has GDAL 3.13, Shapely 2.0, pyproj 3.6 — enough to run every script here.

## Sample data is missing, and is not in this repo at all

This copy ships **no** data, and neither does the GDAL copy of Chapter 04. Only one input exists anywhere in the archive:

- `TM_WORLD_BORDERS-0.3.shp` — copy it from `../../GDAL/Python Geospatial Development/Chapter 03/` (also `GDAL/Mapnik/`) into your working directory. Needed by `calcBoundingBoxes.py`, `calcCommonBorder.py`, `calcFeatureLengths.py`, `calcBorderLength.py`.

Still absent, so these scripts cannot run until you supply data:

- `changeDatum.py` → `roads/roads.shp` (NAD27); `changeProjection.py` → `miami/miami.shp` (UTM 17).
- `histogram.py` → `l10g` raster; hardcoded bbox over Tasmania (-48..-33 lat, 165..179 long), Int16.
- `findShoshone.py`, `findNearbyParks.py` → `CA_Features_XXXX.txt`. `XXXX` is a literal placeholder from the book; substitute a real USGS/TIGER `CA_Features_*.txt` (pipe-delimited) and rename the reference. `findNearbyParks.py` also needs `tl_2015_us_cbsa.shp`.

## Known failures (book-era code, not setup bugs to chase)

- Missing input shows up as `AttributeError: 'NoneType' object has no attribute 'GetLayer'` / `GetRasterBand`, because `ogr.Open` and `gdal.Open` return `None` instead of raising. `CA_Features_XXXX.txt` instead gives `FileNotFoundError`.
- `calcFeatureLengths.py` is a **byte-identical copy of `calcCommonBorder.py`** (the book's copy-paste bug): same Thailand/Myanmar border code, prints nothing, writes `common-border/`. The real per-feature length script is `calcBorderLength.py`, whose usage message still says `calcFeatureLengths.py`. Don't "fix" the duplicate by rewriting it into a length calculator without being asked — flag it.
- `calcBorderLength.py` uses `pyproj.transform`, deprecated in pyproj 3.6 (FutureWarning). It works, and it reports km per feature index.
- `ogr` emits a `FutureWarning` about `UseExceptions()` under GDAL 3.13. Harmless noise.

## Destructive side effects

These `shutil.rmtree` then recreate an output directory in the cwd, so back up anything you care about:

- `calcCommonBorder.py`, `calcFeatureLengths.py` → `common-border/`
- `changeDatum.py` → `roads-reprojected/`
- `changeProjection.py` → `miami-reprojected/`

## Duplicates

All nine files are byte-identical to `../../GDAL/Python Geospatial Development/Chapter 04/Windows/`. A fix in one copy does not reach the other; check both before editing.
