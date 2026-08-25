import streamlit as st
import pandas as pd
import json
import plotly.graph_objects as go

# =========================
# PAGE
# =========================

st.set_page_config(
    page_title="India Social Explorer",
    page_icon="🇮🇳",
    layout="wide"
)

# =========================
# PASTEL DESIGN
# =========================

st.markdown("""
<style>

@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=Playfair+Display:wght@500;600&display=swap');

.stApp {
    background: #FFF9F5;
    color: #4A4545;
    font-family: 'DM Sans', sans-serif;
}

h1 {
    font-family: 'Playfair Display', serif !important;
    color: #6B5B73 !important;
    font-size: 3rem !important;
}

h2, h3 {
    color: #6B5B73 !important;
}

[data-testid="stMetric"] {
    background: #FFFFFF;
    border: 1px solid #EADFE3;
    border-radius: 20px;
    padding: 20px;
    box-shadow: 0 5px 18px rgba(100,80,90,0.08);
}

[data-testid="stMetricLabel"] {
    color: #9A8494 !important;
}

[data-testid="stMetricValue"] {
    color: #6B5B73 !important;
}

[data-testid="stDataFrame"] {
    border-radius: 15px;
}

hr {
    border-color: #E8DDE0 !important;
}

.state-card {
    background: #FFFFFF;
    border: 1px solid #EADFE3;
    border-radius: 22px;
    padding: 25px;
    margin-top: 10px;
    box-shadow: 0 5px 18px rgba(100,80,90,0.07);
}

.state-name {
    font-family: 'Playfair Display', serif;
    font-size: 2rem;
    color: #6B5B73;
    margin-bottom: 15px;
}

</style>
""", unsafe_allow_html=True)

# =========================
# LOAD DATA
# =========================

df = pd.read_csv("data/state_literacy.csv")

df["state_clean"] = (
    df["state"]
    .str.replace("State - ", "", regex=False)
    .str.strip()
)

# =========================
# TITLE
# =========================

st.title("🇮🇳 India Social Explorer")

st.markdown(
    "### A visual journey through India's literacy landscape · Census 2011"
)

# =========================
# SUMMARY
# =========================

total_population = df["population"].sum()
total_literate = df["literate"].sum()

total_male_population = df["male_population"].sum()
total_female_population = df["female_population"].sum()

total_male_literate = df["male_literate"].sum()
total_female_literate = df["female_literate"].sum()

overall_literacy = (
    total_literate / total_population * 100
)

male_literacy = (
    total_male_literate / total_male_population * 100
)

female_literacy = (
    total_female_literate / total_female_population * 100
)

col1, col2, col3, col4 = st.columns(4)

col1.metric(
    "🇮🇳 Population",
    f"{total_population:,.0f}"
)

col2.metric(
    "📚 Literacy Rate",
    f"{overall_literacy:.1f}%"
)

col3.metric(
    "👨 Male Literacy",
    f"{male_literacy:.1f}%"
)

col4.metric(
    "👩 Female Literacy",
    f"{female_literacy:.1f}%"
)

st.divider()

# =========================
# STATE EXPLORER
# =========================

st.subheader("🌸 Explore a State")

selected_state = st.selectbox(
    "Choose a state",
    sorted(df["state_clean"].unique())
)

state_data = df[
    df["state_clean"] == selected_state
].iloc[0]

st.markdown(
    f"""
    <div class="state-card">
        <div class="state-name">🌷 {selected_state}</div>
    </div>
    """,
    unsafe_allow_html=True
)

col1, col2, col3, col4 = st.columns(4)

col1.metric(
    "👥 Population",
    f"{state_data['population']:,.0f}"
)

col2.metric(
    "📚 Literacy",
    f"{state_data['literacy_rate']:.1f}%"
)

state_male_rate = (
    state_data["male_literate"]
    / state_data["male_population"]
    * 100
)

state_female_rate = (
    state_data["female_literate"]
    / state_data["female_population"]
    * 100
)

col3.metric(
    "👨 Male Literacy",
    f"{state_male_rate:.1f}%"
)

col4.metric(
    "👩 Female Literacy",
    f"{state_female_rate:.1f}%"
)

st.divider()

# =========================
# MAP
# =========================

st.subheader("🗺️ Literacy Across India")

with open(
    "maps/india_states.geojson",
    "r",
    encoding="utf-8"
) as f:
    geo = json.load(f)

for feature in geo["features"]:

    map_state = feature["properties"]["state_name_harmonized"]

    match = df[
        df["state_clean"].str.upper()
        == map_state.strip().upper()
    ]

    if not match.empty:
        feature["properties"]["literacy"] = float(
            match.iloc[0]["literacy_rate"]
        )
    else:
        feature["properties"]["literacy"] = None

locations = [
    feature["properties"]["state_name_harmonized"]
    for feature in geo["features"]
]

values = [
    feature["properties"]["literacy"]
    for feature in geo["features"]
]

fig = go.Figure(
    go.Choroplethmap(
        geojson=geo,
        locations=locations,
        z=values,
        featureidkey="properties.state_name_harmonized",

        colorscale=[
            [0.0, "#E8DFF5"],
            [0.25, "#D8E2F3"],
            [0.5, "#CDE8E1"],
            [0.75, "#F5D6D0"],
            [1.0, "#E9BFC7"]
        ],

        zmin=60,
        zmax=95,

        marker_line_color="white",
        marker_line_width=1,

        colorbar_title="Literacy (%)",

        hovertemplate=
            "<b>%{location}</b><br>"
            "Literacy: %{z:.2f}%"
            "<extra></extra>"
    )
)

fig.update_layout(
    map_style="carto-positron",
    map_zoom=3.8,
    map_center={
        "lat": 22.5,
        "lon": 79
    },
    height=650,
    margin=dict(
        l=0,
        r=0,
        t=20,
        b=0
    )
)

st.plotly_chart(
    fig,
    use_container_width=True
)

# =========================
# TOP & BOTTOM
# =========================

st.subheader("📊 Literacy Leaders & Laggards")

col1, col2 = st.columns(2)

with col1:

    st.markdown("### 🏆 Highest Literacy")

    top5 = (
        df[
            ["state_clean", "literacy_rate"]
        ]
        .sort_values(
            "literacy_rate",
            ascending=False
        )
        .head(5)
    )

    top5.columns = [
        "State",
        "Literacy %"
    ]

    st.dataframe(
        top5,
        hide_index=True,
        use_container_width=True
    )

with col2:

    st.markdown("### 📉 Lowest Literacy")

    bottom5 = (
        df[
            ["state_clean", "literacy_rate"]
        ]
        .sort_values(
            "literacy_rate",
            ascending=True
        )
        .head(5)
    )

    bottom5.columns = [
        "State",
        "Literacy %"
    ]

    st.dataframe(
        bottom5,
        hide_index=True,
        use_container_width=True
    )

# =========================
# FULL TABLE
# =========================

st.divider()

st.subheader("📋 State-wise Data")

display_df = df[
    [
        "state_clean",
        "population",
        "male_population",
        "female_population",
        "literate",
        "male_literate",
        "female_literate",
        "literacy_rate"
    ]
].copy()

display_df.columns = [
    "State",
    "Population",
    "Male Population",
    "Female Population",
    "Literate Population",
    "Male Literates",
    "Female Literates",
    "Literacy Rate (%)"
]

st.dataframe(
    display_df,
    hide_index=True,
    use_container_width=True
)
