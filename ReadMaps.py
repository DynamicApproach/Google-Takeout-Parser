#!/usr/bin/env python3
import folium
import math
from collections import Counter
from folium.plugins import MarkerCluster
from datetime import datetime
import folium.utilities as util
import json
import csv
import glob
import concurrent.futures
import os
import tkinter as tk
from tkinter import filedialog
import argparse

def main():
    parser = argparse.ArgumentParser(description="Generate a map from Google Location History data.")
    parser.add_argument("--file", "-f", help="Specifies the file path to your Google Location History JSON file.", required=True)
    parser.add_argument("--start-date", "-s", help="Specifies the start date (inclusive) for the data to include in the map. The date should be in YYYY-MM-DD format (e.g., '2021-01-01').", required=True)
    parser.add_argument("--end-date", "-e", help="Specifies the end date (exclusive) for the data to include in the map. The date should be in YYYY-MM-DD format (e.g., '2022-01-01').", required=True)
    parser.add_argument("--output-file", "-o", help="Specifies the file path for the generated HTML map.", default="map.html")
    parser.add_argument("--include-path", "-p", help="Specifies whether to include the paths between locations in the map.", action="store_true")
    parser.add_argument("--path-color", "-c", help="Specifies the color to use for the paths between locations. The color should be specified in hex format (e.g., '#ff0000' for red).", default="#3388ff")
    parser.add_argument("--cluster-markers", "-m", help="Specifies whether to cluster the markers on the map.", action="store_true")
    args = parser.parse_args()

    # Set the file path to the JSON file
    json_file = args.file

    # Set the start and end dates for the data
    start_date = args.start_date
    end_date = args.end_date

    # Set the output file path for the generated map
    output_file = args.output_file

    # Determine whether to include paths between locations
    include_path = args.include_path

    # Set the color for the paths between locations
    path_color = args.path_color

    # Determine whether to cluster markers
    cluster_markers = args.cluster_markers

    # Generate the map
    generate_map(json_file, output_file, start_date, end_date, include_path, path_color, cluster_markers)
def main():
    parser = argparse.ArgumentParser(description="Generate a map from Google Location History data.")
    parser.add_argument("--file", "-f", help="Specifies the file path to your Google Location History JSON file.", required=True)
    parser.add_argument("--start-date", "-s", help="Specifies the start date (inclusive) for the data to include in the map. The date should be in YYYY-MM-DD format (e.g., '2021-01-01').", required=True)
    parser.add_argument("--end-date", "-e", help="Specifies the end date (exclusive) for the data to include in the map. The date should be in YYYY-MM-DD format (e.g., '2022-01-01').", required=True)
    parser.add_argument("--output-file", "-o", help="Specifies the file path for the generated HTML map.", default="map.html")
    parser.add_argument("--include-path", "-p", help="Specifies whether to include the paths between locations in the map.", action="store_true")
    parser.add_argument("--path-color", "-c", help="Specifies the color to use for the paths between locations. The color should be specified in hex format (e.g., '#ff0000' for red).", default="#3388ff")
    parser.add_argument("--cluster-markers", "-m", help="Specifies whether to cluster the markers on the map.", action="store_true")
    args = parser.parse_args()

    # Set the file path to the JSON file
    json_file = args.file

    # Set the start and end dates for the data
    start_date = args.start_date
    end_date = args.end_date

    # Set the output file path for the generated map
    output_file = args.output_file

    # Determine whether to include paths between locations
    include_path = args.include_path

    # Set the color for the paths between locations
    path_color = args.path_color

    # Determine whether to cluster markers
    cluster_markers = args.cluster_markers

    # Generate the map
    generate_map(json_file, output_file, start_date, end_date, include_path, path_color, cluster_markers)


# Function to parse JSON data and return a list of dictionaries
def parse_json_data(data):
    rows = []
    for obj in data["timelineObjects"]:
        if "activitySegment" in obj:
            segment = obj["activitySegment"]
            if "startLocation" not in segment or "endLocation" not in segment:
                continue

            start_location = segment["startLocation"]
            end_location = segment["endLocation"]
            duration = segment["duration"]
            activities = segment["activities"]

            for activity in activities:
                if (
                    "latitudeE7" in start_location
                    and "longitudeE7" in start_location
                    and "latitudeE7" in end_location
                    and "longitudeE7" in end_location
                ):
                    row = {
                        "start_latitude": start_location["latitudeE7"],
                        "start_longitude": start_location["longitudeE7"],
                        "end_latitude": end_location["latitudeE7"],
                        "end_longitude": end_location["longitudeE7"],
                        "start_timestamp": duration["startTimestamp"],
                        "end_timestamp": duration["endTimestamp"],
                        "activity_type": activity["activityType"],
                        "probability": activity["probability"],
                    }
                    rows.append(row)
        elif "placeVisit" in obj:
            visit = obj["placeVisit"]
            if "location" not in visit:
                continue
            location = visit["location"]
            duration = visit["duration"]
            if (
                "latitudeE7" in location
                and "longitudeE7" in location
                and "startTimestamp" in duration
                and "endTimestamp" in duration
            ):
                row = {
                    "start_latitude": location["latitudeE7"],
                    "start_longitude": location["longitudeE7"],
                    "end_latitude": location["latitudeE7"],
                    "end_longitude": location["longitudeE7"],
                    "start_timestamp": duration["startTimestamp"],
                    "end_timestamp": duration["endTimestamp"],
                    "activity_type": "PLACE_VISIT",
                    "probability": None,
                }
                rows.append(row)
    return rows

def ask_for_directory():
    root = tk.Tk()
    root.withdraw()
    folder_selected = filedialog.askdirectory()
    return folder_selected
def ask_for_file():
    root = tk.Tk()
    root.withdraw()
    file_path = filedialog.askopenfilename()
    return file_path


# Define the paths to search for JSON files


def process_json_file(json_file):
    with open(json_file, "r", encoding="utf-8", errors="replace") as f:
        data = json.load(f)
        return parse_json_data(data)

selected_folder = ask_for_directory()
path_pattern = os.path.join(selected_folder, "Location History", "Semantic Location History", "*", "*.json")

all_data = []
json_files = glob.glob(path_pattern)

# Use a ThreadPoolExecutor to process JSON files concurrently
with concurrent.futures.ThreadPoolExecutor() as executor:
    results = list(executor.map(process_json_file, json_files))

    for result in results:
        all_data.extend(result)

# Write the data to a CSV file
csv_file = "combined_data.csv"
csv_columns = ["start_latitude", "start_longitude", "end_latitude", "end_longitude", "start_timestamp", "end_timestamp", "activity_type", "probability"]

with open(csv_file, "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=csv_columns)
    writer.writeheader()
    for data in all_data:
        writer.writerow(data)


# Aggregate location data
locations = []
for row in all_data:
    locations.append((row["start_latitude"] / 1e7, row["start_longitude"] / 1e7))
    locations.append((row["end_latitude"] / 1e7, row["end_longitude"] / 1e7))

# Find the most active locations
location_count = Counter(locations)
top_locations = location_count.most_common(250)  # Adjust the number to show more or less locations


# Create the map centered on the first top location
latitude, longitude = top_locations[0][0]
map = folium.Map(location=[latitude, longitude], zoom_start=12)

# Function to compute the circle radius based on the map's zoom level
def compute_radius(zoom, count):
    base_radius = 10 * math.log(count + 1)
    return base_radius * (1 / (1 << (15 - zoom)))

# Create a MarkerCluster
marker_cluster = MarkerCluster().add_to(map)

def convert_to_local_time(timestamp_str):
    try:
        dt = datetime.strptime(timestamp_str, '%Y-%m-%dT%H:%M:%S.%fZ')
    except ValueError:
        dt = datetime.strptime(timestamp_str, '%Y-%m-%dT%H:%M:%SZ')
    return dt.strftime('%Y-%m-%d %H:%M:%S')


# Add bubbles to the map for the most active locations
initial_zoom = 12
for location, count in top_locations:
    lat, lng = location

    # Get the row associated with the current location
    row = next((row for row in all_data if (row["start_latitude"] / 1e7, row["start_longitude"] / 1e7) == location), None)
    if row:
        if 'end_timestamp' in row:
            start_time = convert_to_local_time(row['start_timestamp'])
            end_time = convert_to_local_time(row['end_timestamp'])
            activity_type = row['activity_type']
        else:
            start_time = convert_to_local_time(row['start_timestamp'])
            end_time = 'N/A'
            activity_type = 'N/A'
        activity_type = row["activity_type"]
    else:
        start_time = "N/A"
        end_time = "N/A"
        activity_type = "N/A"

    popup_text = f"Location: {lat:.6f}, {lng:.6f}<br>Time: {start_time} - {end_time}<br>Date: {start_time[:10]}<br>Method of travel: {activity_type}"
    popup = folium.Popup(popup_text, max_width=300)

    folium.CircleMarker(
        location=[lat, lng],
        radius=compute_radius(initial_zoom, count),
        fill=True,
        fill_opacity=0.7 / math.log(count + 2),
        color="blue",
        fill_color="blue",
        popup=popup,
    ).add_to(marker_cluster)

# Connect the dots with lines based on their order in the dataset
# and update zoom opacity
zoom_opacity_function = '''
function updateOpacity(zoom) {
    var opacity = (15 - zoom) / 15;
    {% for line_id in line_ids %}
        var line = document.getElementById('{{ line_id }}');
        line.setAttribute('stroke-opacity', opacity);
    {% endfor %}
}

map.on('zoomend', function() {
    updateOpacity(map.getZoom());
});
'''

line_ids = []  # Add this line to keep track of the line_ids

unique_lines = set()
for i in range(len(locations) - 1):
    start_location = locations[i]
    end_location = locations[i + 1]
    
    # Add the line only if it doesn't exist in the unique_lines set
    if (start_location, end_location) not in unique_lines:
        folium.PolyLine(
            locations=[start_location, end_location],
            color="green",
            weight=.5,
        ).add_to(map)
        
        # Add the current line to the unique_lines set
        unique_lines.add((start_location, end_location))

# Save the map to an HTML file
map.save("most_active_locations.html")

