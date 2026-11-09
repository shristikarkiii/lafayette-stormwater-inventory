"""Inventory schema, transcribed from docs/data_dictionary.md.

build_gdb.py builds the geodatabase from these definitions, and the schema
test (Day 7) checks that this file and the data dictionary still agree.
"""

GDB_NAME = "stormwater.gdb"
EPSG = 3452  # NAD83 / Louisiana South (ftUS)

# name -> (description, {code: value})
DOMAINS = {
    "dCondition": ("Structural condition", {
        1: "Good", 2: "Fair", 3: "Poor", 9: "Can't assess"}),
    "dDebris": ("Share of opening blocked", {
        0: "None", 1: "Light (<25%)", 2: "Moderate (25-50%)",
        3: "Heavy (>50%)"}),
    "dDefect": ("Most serious visible defect", {
        0: "None", 1: "Cracked or broken concrete",
        2: "Damaged or loose grate", 3: "Missing grate or lid",
        4: "Settlement or sinkhole nearby", 5: "Other"}),
    "dLidLabel": ("Text cast in manhole lid", {
        1: "Storm", 2: "Sewer", 3: "Other utility", 4: "Unmarked"}),
    "dOwner": ("Responsible party", {
        1: "City (LCG)", 2: "State (LA DOTD)", 3: "University (ULL)",
        4: "Private", 9: "Unknown"}),
    "dYesNo": ("Yes or no", {0: "No", 1: "Yes"}),
    "dPipeMaterial": ("Pipe material", {
        1: "Concrete", 2: "Corrugated metal", 3: "Plastic (HDPE/PVC)",
        9: "Unknown"}),
    "dFlow": ("Flow at time of visit", {0: "Dry", 1: "Trickle", 2: "Flowing"}),
    "dChannelType": ("Open channel type", {
        1: "Roadside ditch", 2: "Grass swale", 3: "Concrete lined"}),
    "dAction": ("Follow-up needed", {
        0: "None", 1: "Cleaning needed", 2: "Repair needed",
        3: "Refer to other owner"}),
}

# Field tuple: (name, type, alias, length, domain)
_ID = ("FACILITYID", "TEXT", "Facility ID", 12, None)
_NOTES = ("NOTES", "TEXT", "Notes", 255, None)
_ACC = ("HORIZ_ACC_M", "DOUBLE", "Horizontal accuracy (m)", None, None)

# name -> (geometry type or None for a table, alias, fields)
TABLES = {
    "StormInlet": ("POINT", "Storm inlet", [
        _ID,
        ("INLETTYPE", "SHORT", "Inlet type", None, None),  # subtype field
        ("CONDITION", "SHORT", "Condition", None, "dCondition"),
        ("DEBRIS", "SHORT", "Debris", None, "dDebris"),
        ("STANDINGWATER", "SHORT", "Standing water", None, "dYesNo"),
        ("DEFECT", "SHORT", "Defect", None, "dDefect"),
        ("LIDLABEL", "SHORT", "Lid label", None, "dLidLabel"),
        ("OWNER", "SHORT", "Owner", None, "dOwner"),
        ("LOCDESC", "TEXT", "Location description", 100, None),
        ("STREETNAME", "TEXT", "Street name", 50, None),
        _NOTES,
        _ACC,
        ("REQ_COUNT", "SHORT", "Drainage requests 2016-2020", None, None),
        ("PRIORITY", "DOUBLE", "Inspection priority", None, None),
    ]),
    "StormOutfall": ("POINT", "Storm outfall", [
        _ID,
        ("MATERIAL", "SHORT", "Pipe material", None, "dPipeMaterial"),
        ("CONDITION", "SHORT", "Condition", None, "dCondition"),
        ("FLOW", "SHORT", "Flow", None, "dFlow"),
        ("RECEIVING", "TEXT", "Receiving water", 50, None),
        _NOTES,
        _ACC,
    ]),
    "OpenChannel": ("POLYLINE", "Open channel", [
        _ID,
        ("CHANNELTYPE", "SHORT", "Channel type", None, "dChannelType"),
        ("CONDITION", "SHORT", "Condition", None, "dCondition"),
        ("DEBRIS", "SHORT", "Debris", None, "dDebris"),
        _NOTES,
    ]),
    "InletInspection": (None, "Inlet inspection", [
        ("INLET_ID", "TEXT", "Inlet facility ID", 12, None),
        ("INSPDATE", "DATE", "Inspection date", None, None),
        ("CONDITION", "SHORT", "Condition", None, "dCondition"),
        ("DEBRIS", "SHORT", "Debris", None, "dDebris"),
        ("ACTION", "SHORT", "Follow-up action", None, "dAction"),
        _NOTES,
    ]),
}
