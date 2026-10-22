# Data dictionary

Schema for the field inventory. `scripts/build_gdb.py` (Day 4 to 6) builds
the geodatabase from this document, so a change here is a change to the
data model.

- **Geodatabase:** file geodatabase, NAD83 / Louisiana South (ftUS), EPSG 3452
- **Field names:** upper case, no spaces, at most 31 characters
- **Required** fields must be filled before a feature can be saved in the
  field form; attribute rules enforce the same in the geodatabase
- **Automatic** fields are filled by the geodatabase, ArcGIS Field Maps or an
  attribute rule, never typed

## Feature classes

| Feature class | Geometry | What it holds |
|---|---|---|
| `StormInlet` | Point | Curb openings, grate inlets, combination inlets and manholes |
| `StormOutfall` | Point | Pipe ends discharging to a ditch or coulee |
| `OpenChannel` | Polyline | Roadside ditches, swales and lined channels |
| `InletInspection` | Table | Repeat inspections of an inlet (Survey123, Day 22) |

All three feature classes have **attachments enabled** for photos and
**editor tracking** on (`created_user`, `created_date`, `last_edited_user`,
`last_edited_date`).

## StormInlet

Subtype field: `INLETTYPE`.

| Field | Type | Domain | Req. | Source | Description |
|---|---|---|---|---|---|
| `FACILITYID` | Text (12) | | Yes | Automatic | Unique ID, `INL-0001` upward (attribute rule) |
| `INLETTYPE` | Short | Subtypes below | Yes | Field | Kind of structure |
| `CONDITION` | Short | `dCondition` | Yes | Field | Overall structural condition |
| `DEBRIS` | Short | `dDebris` | Yes | Field | Share of the opening blocked |
| `STANDINGWATER` | Short | `dYesNo` | Yes | Field | Ponded water at the inlet at time of visit |
| `DEFECT` | Short | `dDefect` | Yes | Field | Most serious visible defect |
| `LIDLABEL` | Short | `dLidLabel` | Manholes only | Field | Text cast in the lid |
| `OWNER` | Short | `dOwner` | Yes | Field | Responsible party, best judgement |
| `LOCDESC` | Text (100) | | No | Field | Short location note, e.g. "NE corner, Oakview at Twin Oaks" |
| `STREETNAME` | Text (50) | | No | Automatic | Nearest street centerline (attribute rule) |
| `NOTES` | Text (255) | | No | Field | Anything the domains do not capture |
| `HORIZ_ACC_M` | Double | | No | Automatic | GNSS horizontal accuracy in metres, from Field Maps |
| `REQ_COUNT` | Short | | No | Analysis | City drainage requests within 15 m, 2016 to 2020 (Day 19) |
| `PRIORITY` | Double | | No | Analysis | Inspection priority score (Day 20) |

Attachment: **1 photo required**, taken from the curb looking at the inlet.

### Subtypes (`INLETTYPE`)

| Code | Subtype | Identify by | `LIDLABEL` |
|---|---|---|---|
| 1 | Curb opening | Horizontal slot in the face of the curb, no grate | Not used |
| 2 | Grate inlet | Metal grate in the gutter or pavement, no curb slot | Not used |
| 3 | Combination | Curb slot and grate together | Not used |
| 4 | Manhole | Round lid, curb or sidewalk only; never enter the roadway | Required |

## StormOutfall

| Field | Type | Domain | Req. | Source | Description |
|---|---|---|---|---|---|
| `FACILITYID` | Text (12) | | Yes | Automatic | `OUT-001` upward |
| `MATERIAL` | Short | `dPipeMaterial` | Yes | Field | Pipe material |
| `CONDITION` | Short | `dCondition` | Yes | Field | Overall structural condition |
| `FLOW` | Short | `dFlow` | Yes | Field | Flow at time of visit |
| `RECEIVING` | Text (50) | | No | Field | Receiving water, e.g. "Coulee Mine" |
| `NOTES` | Text (255) | | No | Field | |
| `HORIZ_ACC_M` | Double | | No | Automatic | GNSS horizontal accuracy (m) |

Flow in dry weather (no rain for 72 hours) is recorded because it is the
standard first screen for illicit discharges in municipal stormwater (MS4)
programs; note the weather on each field day in the session log.

## OpenChannel

| Field | Type | Domain | Req. | Source | Description |
|---|---|---|---|---|---|
| `FACILITYID` | Text (12) | | Yes | Automatic | `CH-001` upward |
| `CHANNELTYPE` | Short | `dChannelType` | Yes | Field | |
| `CONDITION` | Short | `dCondition` | Yes | Field | |
| `DEBRIS` | Short | `dDebris` | Yes | Field | Share of the channel cross-section blocked |
| `NOTES` | Text (255) | | No | Field | |

## InletInspection (table)

Related to `StormInlet` by `FACILITYID`, one inlet to many inspections.

| Field | Type | Domain | Req. | Description |
|---|---|---|---|---|
| `INLET_ID` | Text (12) | | Yes | `FACILITYID` of the inlet |
| `INSPDATE` | Date | | Yes | |
| `CONDITION` | Short | `dCondition` | Yes | |
| `DEBRIS` | Short | `dDebris` | Yes | |
| `ACTION` | Short | `dAction` | Yes | Follow-up needed |
| `NOTES` | Text (255) | | No | |

## Domains

**`dCondition`** — rate the worst part of the structure.

| Code | Value | Rule of thumb |
|---|---|---|
| 1 | Good | Intact, no cracks beyond hairline, grate seated |
| 2 | Fair | Cracking, spalling or minor settlement; still works as built |
| 3 | Poor | Broken or missing pieces, grate loose or missing, settlement or a hole next to the structure |
| 9 | Can't assess | Covered by a parked car, leaves or water |

**`dDebris`**

| Code | Value |
|---|---|
| 0 | None |
| 1 | Light (under 25% of the opening blocked) |
| 2 | Moderate (25 to 50%) |
| 3 | Heavy (over 50%) |

**`dDefect`**: 0 None · 1 Cracked or broken concrete · 2 Damaged or loose grate · 3 Missing grate or lid · 4 Settlement or sinkhole nearby · 5 Other (describe in `NOTES`)

**`dLidLabel`**: 1 Storm · 2 Sewer · 3 Other utility · 4 Unmarked

**`dOwner`**: 1 City (LCG) · 2 State (LA DOTD) · 3 University (ULL) · 4 Private · 9 Unknown. Inlets along Johnston St (US 167) default to State; inlets inside parking lots to Private.

**`dYesNo`**: 0 No · 1 Yes

**`dPipeMaterial`**: 1 Concrete · 2 Corrugated metal · 3 Plastic (HDPE/PVC) · 9 Unknown

**`dFlow`**: 0 Dry · 1 Trickle · 2 Flowing

**`dChannelType`**: 1 Roadside ditch · 2 Grass swale · 3 Concrete lined

**`dAction`**: 0 None · 1 Cleaning needed · 2 Repair needed · 3 Refer to other owner

## Design choices

- **Coded domains instead of free text.** Every answer that feeds the
  priority score is a pick-list, so the data can be counted without cleaning.
- **Condition and debris are separate.** A sound inlet full of leaves needs a
  crew with a vacuum truck; a clean, broken one needs a repair. One combined
  score would hide which.
- **Three condition levels plus "can't assess".** Field ratings on five-point
  scales drift between visits; three levels with written rules of thumb stay
  consistent, and "can't assess" keeps unknowns from being guessed as Good.
- **No measurements.** Sizes need a tape measure at the curb and would double
  field time; they can be added later as optional fields without changing
  anything above.
- **Manholes at the curb and sidewalk only.** Lids in the travel lane are not
  collected, for safety. `LIDLABEL` separates storm lids from sewer lids, and
  only storm lids are used in the analysis.
