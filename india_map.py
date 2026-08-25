import json
import pandas as pd
import plotly.graph_objects as go

# Load our literacy data
df = pd.read_csv("data/state_literacy.csv")

# Load India map
with open("maps/india_states.geojson", "r", encoding="utf-8") as f:
    geo = json.load(f)

# Put literacy rate into each map state
for feature in geo["features"]:

    map_state = feature["properties"]["state_name_harmonized"]

    # Remove "State -" from our CSV names
    csv_state = df["state"].str.replace(
        "State - ", "", regex=False
    ).str.strip()

    # Find matching state
    match = df[
        csv_state.str.upper() == map_state.strip().upper()
    ]

    if not match.empty:
        feature["properties"]["literacy"] = float(
            match.iloc[0]["literacy_rate"]
        )
    else:
        feature["properties"]["literacy"] = None


# Get state names
locations = [
    feature["properties"]["state_name_harmonized"]
    for feature in geo["features"]
]

# Get literacy values
values = [
    feature["properties"]["literacy"]
    for feature in geo["features"]
]


# Create map
fig = go.Figure(
    go.Choroplethmap(
        geojson=geo,
        locations=locations,
        z=values,
        featureidkey="properties.state_name_harmonized",
        colorscale="Blues",
        zmin=60,
        zmax=95,
        marker_line_color="white",
        marker_line_width=1,
        colorbar_title="Literacy (%)",
        hovertemplate="<b>%{location}</b><br>"
                      "Literacy: %{z:.2f}%"
                      "<extra></extra>"
    )
)


# Map settings
fig.update_layout(
    title="Literacy Across India — Census 2011",
    map_style="carto-positron",
    map_zoom=3.8,
    map_center={
        "lat": 22.5,
        "lon": 79
    },
    width=1100,
    height=750
)

fig.show()
