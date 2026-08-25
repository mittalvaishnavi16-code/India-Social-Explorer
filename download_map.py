import requests
import os

url = "https://raw.githubusercontent.com/saketlab/censusindia/master/inst/extdata/india-census-2011-states.geojson"

os.makedirs("maps", exist_ok=True)

response = requests.get(url)

if response.status_code == 200:
    with open("maps/india_states.geojson", "wb") as file:
        file.write(response.content)

    print("Map downloaded successfully!")
else:
    print("Could not download the map.")
    print("Status code:", response.status_code)
    