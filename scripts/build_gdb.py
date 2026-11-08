"""Build the inventory file geodatabase from scripts/schema.py.

Deletes and recreates data/stormwater.gdb on every run, so the schema in the
repo is the only source of truth. Run with ArcGIS Pro's Python:

    propy scripts/build_gdb.py

Day 4: domains, feature classes, fields and editor tracking.
"""

import os
import shutil
import sys
from pathlib import Path

import arcpy

sys.path.insert(0, str(Path(__file__).resolve().parent))
from schema import DOMAINS, EPSG, GDB_NAME, TABLES  # noqa: E402

ROOT = Path(__file__).resolve().parents[1]
GDB = ROOT / "data" / GDB_NAME


def create_gdb():
    if GDB.exists():
        shutil.rmtree(GDB)  # fails loudly if ArcGIS Pro has it open
    arcpy.management.CreateFileGDB(str(GDB.parent), GDB.name)


def create_domains():
    for name, (desc, values) in DOMAINS.items():
        arcpy.management.CreateDomain(str(GDB), name, desc, "SHORT", "CODED")
        for code, value in values.items():
            arcpy.management.AddCodedValueToDomain(str(GDB), name, code, value)
        print(f"  domain {name}: {len(values)} values")


def create_tables():
    sr = arcpy.SpatialReference(EPSG)
    for name, (geom, alias, fields) in TABLES.items():
        if geom:
            arcpy.management.CreateFeatureclass(
                str(GDB), name, geom, spatial_reference=sr, out_alias=alias)
        else:
            arcpy.management.CreateTable(str(GDB), name, out_alias=alias)
        path = str(GDB / name)
        arcpy.management.AddFields(path, [
            [f, t, a, length or "", "", dom or ""]
            for f, t, a, length, dom in fields])
        arcpy.management.EnableEditorTracking(
            path, "created_user", "created_date", "last_edited_user",
            "last_edited_date", "ADD_FIELDS", "UTC")
        kind = geom.lower() if geom else "table"
        print(f"  {name} ({kind}): {len(fields)} fields")


def main():
    arcpy.env.overwriteOutput = True
    print(f"Building {GDB.relative_to(ROOT)}")
    create_gdb()
    create_domains()
    create_tables()
    print("Done")


if __name__ == "__main__":
    main()
    sys.stdout.flush()
    os._exit(0)  # arcpy can hang on interpreter exit
