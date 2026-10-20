# Lafayette Stormwater Inlet Inventory

A field-collected inventory of storm drain inlets, outfalls and roadside
ditches for a neighborhood in Lafayette, Louisiana, built the way a city
stormwater program would run it: a rule-enforced geodatabase, a mobile
collection form, scripted QA/QC, and a dashboard for prioritizing inspections.

**Status: in progress.** The roadmap is tracked in
[Issues](../../issues) and [Milestones](../../milestones), one step per day.

## Why

Lafayette Consolidated Government publishes outfalls (350), culverts and cross
drains (2,378), waterways, and 4,311 drainage service requests (Aug 2016 to
Mar 2020). It does not publish storm drain inlets, which is where 1,354 of
those requests (catch basin and subsurface pipe problems) begin. This project
fills that gap for one study area and uses the request history to rank which
inlets need inspection first.

## Plan

| Week | Milestone | Deliverables |
|---|---|---|
| 1 | Design | Study area, data dictionary, file geodatabase built by script (domains, subtypes, attribute rules, attachments) |
| 2 | Field collection | Hosted layer, ArcGIS Field Maps form, 3 to 4 field sessions |
| 3 | QA/QC and analysis | Automated QA checks, positional accuracy, inlet drainage areas from lidar, request history, inspection priority |
| 4 | Delivery | ArcGIS Dashboard, Survey123 inspection form, map book, findings |

## Data

| Source | Layer |
|---|---|
| Lafayette Consolidated Government, `maps.lafayettela.gov` | Outfalls, culverts and cross drains, waterways, street centerlines, drainage service requests |
| USGS 3D Elevation Program | 1 m lidar DEM |
| FEMA | National Flood Hazard Layer |
| Field collection (this project) | Inlets, outfalls, ditches, condition, photos |

Drainage service requests are pulled with location, problem type, dates and
status only. Requester and staff contact fields are never downloaded.

## License

Code: MIT. Field data: CC BY 4.0.
