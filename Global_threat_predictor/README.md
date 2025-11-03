# Overview
Global Threat Map is an interactive visualizer of real-time data that converts world event data from the GDELT Project into a dynamic, interactive map of global threat events.
It downloads automatically the most recent dataset, cleans up and normalizes the data, works out mean threat values for all countries, and displays them with colored makers that change values every few minutes.
The project demonstrates real-world data engineering, automation, and visualization skill proficiency, with emphasis on real-world intelligence analysis — exactly the type of workflow utilized in cybersecurity operations centers and data-driven analytics teams.

# How It works!
- Step 1. Every few minutes, the script checks GDELT’s public update file: http://data.gdeltproject.org/gdeltv2/lastupdate.txt That text file always lists the newest global event data files published by GDELT, including political, cyber, and social events happening worldwide. The script automatically finds the latest .export.CSV.zip file, downloads it, and unzips it behind the scenes. You don’t have to download anything manually. the script handles it.

- Step 2. Cleaning and Normalizing the Data. Raw GDELT data uses region-level codes (like USTX for Texas, UKI2 for London, etc.) instead of normal country codes. Before the map can show anything, the script: Extracts only the important columns like SQLDATE, ActionGeo_CountryCode, and GoldsteinScale. Then Converts all regional codes into standard 2-letter ISO country codes for example, USTX → US, RS48 → RU, UKI2 → GB, Drops empty or invalid entries, Converts the event’s GoldsteinScale (which measures impact or tone) into numeric threat levels

- Step 3. Once the data is cleaned, the script groups events by country and calculates the average severity score. Then it labels each country’s risk level based on that score.

- Step 4. Using Folium, the project builds a live global map centered on Earth. Each country with data is marked by a colored circle: Hovering or clicking shows its name, risk label, and score, A small floating legend explains the color meanings, The map updates automatically after every refresh cycle. The map is saved as: threat_map_from_csv.html, You can open it in any web browser.

- Step 5. After building the map, the program waits (default: 10 minutes) and repeats the process: Fetch latest global dataset, Normalize and compute scores, Update the map with new results. This creates a live-updating global threat dashboard. If GDELT’s servers are unreachable, the script automatically falls back to the last saved dataset so your map always loads (I recommend downloading the data if you're having difficulty's and normalizing it with normalization script)

# How to Run It
- Step 1: install required libraries: pip install pandas folium requests
- Step 2: Run the script: python global_threat_predictor.py
- Optional: To disable auto-updating, set this line near the top:
    AUTO_REFRESH = False

# Tech
- Python
- Pandas
- Requests
- Folium
- Zipfile / I/O
- Datetime
