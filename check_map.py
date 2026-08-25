import json

with open("maps/india_states.geojson", "r", encoding="utf-8") as f:
    geo = json.load(f)

print("Number of states:", len(geo["features"]))

print("\nGeometry types:")

for feature in geo["features"]:
    print(
        feature["properties"]["state_name_harmonized"],
        "->",
        feature["geometry"]["type"]
    )
    