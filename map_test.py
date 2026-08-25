import json
import plotly.graph_objects as go

with open("maps/india_states.geojson", "r", encoding="utf-8") as f:
    geo = json.load(f)

feature = geo["features"][0]

coordinates = feature["geometry"]["coordinates"][0]

lon = [point[0] for point in coordinates]
lat = [point[1] for point in coordinates]

fig = go.Figure(
    go.Scattergeo(
        lon=lon,
        lat=lat,
        mode="lines",
        fill="toself"
    )
)

fig.update_geos(
    projection_type="mercator",
    lonaxis_range=[92.5, 93.2],
    lataxis_range=[12.1, 13.1]
)

fig.update_layout(
    title="Andaman & Nicobar Map Test",
    width=900,
    height=700
)

fig.show()
