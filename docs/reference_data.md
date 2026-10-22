# Reference data (Day 2)

`scripts/get_reference.py` pulled Lafayette Consolidated Government's public
drainage layers on 2026-10-21. The snapshot is in
`data/reference/lcg_reference.gpkg` (NAD83 / Louisiana South, ftUS).

| Layer | Within 200 m | Inside study area |
|---|---|---|
| Street centerlines | 120 | 51 |
| Sidewalks | 303 | 132 |
| Culverts and cross drains | 0 | 0 |
| Span cross drains | 0 | 0 |
| Minor waterways | 3 | 1 (Coulee Mine) |
| Major waterways | 0 | 0 |
| Drainage service requests (2016 to 2020) | 40 | 21 |

## What it shows

**The city publishes no drainage structures here.** Its culvert, cross drain
and outfall layers cover roadside-ditch areas; this curb-and-gutter
neighborhood has none within 200 m. The field inventory is the only
structure data for the area.

**The 21 requests come from 10 locations.** One inlet on Whittington Dr
accounts for 12 of them: 10 between May 2017 and Aug 2019 (blockages,
flushes and one cross drain blockage), then 2 more blockages about 1.5 m
away in Dec 2019 and Jan 2020. A second location, Oakview Blvd at Twin Oaks
Blvd, has 2. Repeat requests at one point mark a chronic problem inlet, and
both are priority stops in the field.

**Imagery cannot replace field collection.** Reviewing catch basin requests
on 2023 aerial imagery at 1:400 in ArcGIS Pro:

- Inlets were not identifiable at the imagery's resolution, even at open
  curbs.
- Several request points sit under dense tree canopy, which hides the curb
  entirely.
- Request points are placed at the reported address, not at the structure:
  one sits on a sidewalk beside a parking lot, others at driveways.

So request locations are approximate, and inlet locations have to come from
the field.
