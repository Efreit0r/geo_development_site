# AGENTS.md — Chapter 03

Archive of book exercises, not a buildable project: no git, tests, linter, or dependency manifest. "Verify" means running one script. Archive-wide notes live in `../../../AGENTS.md`.

## What's here

- Standalone book examples: GDAL/OGR, `pyproj`, Shapely, Mapnik.
- `slides.md` — a self-contained Slidev deck (Russian, beginner-level) walking through these scripts. Run with `npx @slidev/cli slides.md`; no assets or config needed. Inline SVG/emoji only, so keep new slides free of external images.
- This copy ships **no sample data** — no raster, no `TM_WORLD_BORDERS-0.3.shp`, no `test-shapefile/`. The duplicate at `../../GDAL/Python Geospatial Development/Chapter 03/` does have the world-borders shapefile.
- System `python3` (3.12) has GDAL 3.13, pyproj 3.6, Shapely 2.0, NumPy. `mapnik` is **not** installed.

## Run / verify

Paths are relative, so always `cd` into the directory that holds the data first.

- `writeRaster.py` → creates `Example Raster.tiff` (360×180 Int16, WGS84, random 1–100 values) in the current directory. Run it before `readRaster.py`.
- `writeVector.py` → creates `test-shapefile/shapefile.shp` with 100 random points. Run it before `readVector.py`. It `shutil.rmtree`s any existing `test-shapefile/` — back that up if it matters.
- `pyproj_example.py` and `shapely_example.py` run as-is.

## Known failures (book-era code, not setup bugs to chase)

- `readRaster.py`: the NumPy branch loops `range(band.XSize)` over rows, so it ends in `IndexError: index 180 is out of bounds ... size 180` on the raster it generates. The struct branch output printed before the traceback is correct. A trimmed, working variant exists at `../../GDAL/readRaster/readRaster.py`.
- `mapnik_example.py`: `import mapnik` fails, the code targets the legacy mapnik 2 API, and it needs `TM_WORLD_BORDERS-0.3.shp` from the GDAL copy.
- `pyproj_example.py`: `pyproj.transform` is deprecated (FutureWarning); the printed text says "UTM zone 17" but the code uses zone 11.
- Missing input files surface as `'NoneType' object has no attribute ...`, because `gdal.Open` / `ogr.Open` return `None` instead of raising.

## Duplicates

- These scripts are near-identical to `../../GDAL/Python Geospatial Development/Chapter 03/` (`readRaster.py` differs only in whitespace). Fixes in one copy do not reach the other.
- `../../GDAL/writeVector/pyproj.py` is a copy of the example script, not a module; it shadows the real `pyproj` package when running from that directory.
