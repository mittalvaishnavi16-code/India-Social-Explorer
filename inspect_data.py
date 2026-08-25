import pandas as pd

file_path = "data/DDW-0000C-08.xlsx"

df = pd.read_excel(
    file_path,
    sheet_name="C-08",
    header=None
)

print("Dataset shape:")
print(df.shape)

print("\nFirst 15 rows and first 10 columns:")
print(df.iloc[:15, :10].to_string())
print("\nColumn structure:")
print(df.iloc[:6, :].to_string())
print("\nRows where Area Name is INDIA:")
print(df[df[3] == "INDIA"].iloc[:10, :15].to_string())
print("\nFirst 50 area names and codes:")
print(
    df[[1, 2, 3, 4, 5]]
    .drop_duplicates()
    .head(50)
    .to_string(index=False)
)
state_rows = df[
    (df[2] == "000") &
    (df[4] == "Total") &
    (df[5] == "All ages")
]

print("\nState-level total rows:")
print(state_rows[[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14]].to_string(index=False))
