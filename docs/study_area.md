# Study area

`data/study_area.geojson`: a 700 m x 700 m square (0.49 km²) west of the
University of Louisiana at Lafayette campus, covering Twin Oaks Blvd,
Ronald Blvd, Oakview Blvd, Catherine St, Whittington Dr, Creamery St and the
Johnston St frontage between them.

## How it was chosen

1. Lafayette's 4,311 drainage service requests (Aug 2016 to Mar 2020) were
   counted on a 1 km grid. Catch basin and subsurface pipe requests (1,354
   citywide) mark curb-and-gutter neighborhoods, where inlets are; the more
   common roadside ditch requests mark areas without them.
2. The cell west of campus was one of the densest for those requests: 27 in
   1 km², against a citywide average well under 10.
3. A full 1 km² cell holds 14 km of streets, too much for three or four
   45-minute field sessions. The square was cut to 700 m, centred on the
   median location of those requests. It keeps 19 catch basin and pipe
   requests and 7.1 km of streets.

| Size | Catch basin / pipe requests | Street length |
|---|---|---|
| 600 m | 12 | 5.1 km |
| **700 m (chosen)** | **19** | **7.1 km** |
| 800 m | 22 | 9.3 km |

## Field notes

- Johnston St (US 167) is a principal arterial and a state route. Inlets
  along it are recorded from the sidewalk only, and may belong to LA DOTD
  rather than the city; the owner field records that.
- The city's 350 published outfalls all lie at least 1.3 km away, along the
  larger coulees. Field data is compared with the city's culvert and cross
  drain layer instead (issue #17).
