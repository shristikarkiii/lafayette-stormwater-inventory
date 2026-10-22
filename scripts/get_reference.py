"""Download Lafayette Consolidated Government drainage layers for the study area.

Pulls each layer from the city's public ArcGIS Server, keeps only features
within BUFFER_M of the study area, and writes them all to one GeoPackage in
NAD83 / Louisiana South (ftUS), the CRS the geodatabase will use.

Drainage service requests are reduced to a short list of fields. The source
layer also holds requester and staff names, phone numbers, e-mail addresses
and free-text notes; those fields are never requested.

Usage:
    python scripts/get_reference.py
"""

from pathlib import Path

import geopandas as gpd
import pandas as pd
import requests

ROOT = Path(__file__).resolve().parents[1]
STUDY_AREA = ROOT / "data" / "study_area.geojson"
OUT = ROOT / "data" / "reference" / "lcg_reference.gpkg"

SERVER = "https://maps.lafayettela.gov/arcgis/rest/services"
CRS = 3452  # NAD83 / Louisiana South (ftUS)
BUFFER_M = 200

# output layer -> (service path, fields to keep; "*" keeps all)
LAYERS = {
    "streets": ("BaseLayers/StreetCenterline/FeatureServer/0",
                "FULL_STR_NAME,FUNC_STR_CLASS"),
    "sidewalks": ("BaseLayers/LCG_Sidewalks/FeatureServer/0", "*"),
    "culverts": ("BaseLayers/LCG_Culvert_Xdrains/FeatureServer/0", "*"),
    "span_crossdrains": ("BaseLayers/LCG_Span_Xdrains/FeatureServer/0", "*"),
    "minor_waterways": ("BaseLayers/LCG_MinorWaterways/FeatureServer/0", "*"),
    "major_waterways": ("BaseLayers/LCG_MajorWaterways/FeatureServer/0", "*"),
    "drainage_requests": ("CW_DrainageRequests/MapServer/0",
                          "REQUESTID,PROBLEMCODE,DESCRIPTION,PRIORITY,"
                          "DATETIMEINIT,DATETIMECLOSED,STATUS,STREETNAME"),
}


def query_layer(path, fields, bbox):
    """Fetch every feature intersecting bbox (WGS84), one page at a time."""
    url = f"{SERVER}/{path}/query"
    params = {
        "where": "1=1",
        "geometry": ",".join(map(str, bbox)),
        "geometryType": "esriGeometryEnvelope",
        "inSR": 4326,
        "spatialRel": "esriSpatialRelIntersects",
        "outFields": fields,
        "outSR": 4326,
        "f": "geojson",
        "resultRecordCount": 1000,
    }
    pages, offset = [], 0
    while True:
        r = requests.get(url, params={**params, "resultOffset": offset},
                         timeout=120)
        r.raise_for_status()
        page = r.json()
        if "error" in page:
            raise RuntimeError(f"{path}: {page['error']}")
        feats = page.get("features", [])
        if feats:
            pages.append(gpd.GeoDataFrame.from_features(feats, crs=4326))
        if len(feats) < params["resultRecordCount"]:
            break
        offset += len(feats)
    if not pages:
        return gpd.GeoDataFrame(geometry=[], crs=4326)
    return pd.concat(pages, ignore_index=True)


def main():
    area = gpd.read_file(STUDY_AREA).to_crs(CRS)
    buffered = area.buffer(BUFFER_M / 0.3048006096).union_all()  # ftUS
    bbox = gpd.GeoSeries([buffered], crs=CRS).to_crs(4326).total_bounds

    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.unlink(missing_ok=True)
    area.to_file(OUT, layer="study_area", driver="GPKG")

    for name, (path, fields) in LAYERS.items():
        gdf = query_layer(path, fields, bbox)
        gdf = gdf[gdf.geometry.notna() & ~gdf.geometry.is_empty].to_crs(CRS)
        gdf = gdf[gdf.intersects(buffered)]
        for col in ("DATETIMEINIT", "DATETIMECLOSED"):
            if col in gdf:
                gdf[col] = pd.to_datetime(gdf[col], unit="ms", errors="coerce")
        inside = gdf.intersects(area.union_all()).sum()
        if len(gdf):
            gdf.to_file(OUT, layer=name, driver="GPKG")
        print(f"{name:18s} {len(gdf):5d} within {BUFFER_M} m, "
              f"{inside:5d} inside the study area")

    print(f"Wrote {OUT.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
