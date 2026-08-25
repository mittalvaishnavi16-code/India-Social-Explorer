import pandas as pd

file_path = "data/DDW-0000C-08.xlsx"

df = pd.read_excel(file_path, sheet_name="C-08", header=None)

# State-level "All ages" rows
states = df[
    (df[2] == "000") &
    (df[4] == "Total") &
    (df[5] == "All ages") &
    (df[1] != "00")
].copy()

# State-level "0-6" rows
children = df[
    (df[2] == "000") &
    (df[4] == "Total") &
    (df[5] == "0-6") &
    (df[1] != "00")
].copy()

# Keep only the columns we need
states = states[[1, 3, 6, 7, 8, 12, 13, 14]]
children = children[[1, 6, 7, 8]]

states.columns = [
    "state_code", "state", "population",
    "male_population", "female_population",
    "literate", "male_literate", "female_literate"
]

children.columns = [
    "state_code", "age_0_6",
    "male_age_0_6", "female_age_0_6"
]

# Join the two tables
states = states.merge(children, on="state_code")

# Calculate population aged 7+
states["population_7plus"] = states["population"] - states["age_0_6"]
states["male_7plus"] = states["male_population"] - states["male_age_0_6"]
states["female_7plus"] = states["female_population"] - states["female_age_0_6"]

# Calculate literacy rates
states["literacy_rate"] = states["literate"] / states["population_7plus"] * 100
states["male_literacy"] = states["male_literate"] / states["male_7plus"] * 100
states["female_literacy"] = states["female_literate"] / states["female_7plus"] * 100

# Gender literacy gap
states["gender_gap"] = states["male_literacy"] - states["female_literacy"]

# Round the rates
states[["literacy_rate", "male_literacy", "female_literacy", "gender_gap"]] = (
    states[["literacy_rate", "male_literacy", "female_literacy", "gender_gap"]]
    .round(2)
)

# Save final dataset
states.to_csv("data/state_literacy.csv", index=False)

print("\nDone! Final dataset created.")
print(states[[
    "state",
    "literacy_rate",
    "male_literacy",
    "female_literacy",
    "gender_gap"
]].to_string(index=False))
