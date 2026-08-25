import json

input_file = "maps/india_states.geojson"
output_file = "maps/india_states_fixed.geojson"


def swap_coordinates(coords):
    if isinstance(coords[0], (int, float)):
        return [coords[1], coords[0]]

    return [swap_coordinates(item) for item in coords]


with open(input_file, "r", encoding="utf-8") as f:
    geojson = json.load(f)


for feature in geojson["features"]:
    geometry = feature["geometry"]

    geometry["coordinates"] = swap_coordinates(
        geometry["coordinates"]
    )


with open(output_file, "w", encoding="utf-8") as f:
    json.dump(geojson, f)


print("Map coordinates fixed!")
print("Saved as:", output_file)
