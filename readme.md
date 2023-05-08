# Explore Your Google Location History

This is a simple Python script that allows you to visualize your Google Location History data on an interactive map using the `folium` library. Stores and place visits will be added to the map as markers, and the paths between them will be drawn as lines. You can click on the markers to see more information about the location or path. Hoving an area will show the general amount of time spend there.

## Getting Started

To use this script, you will need to download your Google Location History data as a JSON file. You can do this by following these steps:

1. Go to [Google Takeout](https://takeout.google.com/settings/takeout).
2. Deselect all services except for "Location History".
3. Click "All Location History" to only export data for this product.
4. Choose the file type you want and how you want to receive the data (e.g., email or Drive).
5. Click "Create export".
6. Wait for the export to finish and then download the data.
7. Extract the downloaded archive and note the location of the JSON file.
8. Run the script and follow the prompts to select your Takeout folder.

## Usage

To use this script, first make sure you have installed all the required libraries by running `pip install -r requirements.txt`.

Next, run the script and follow the prompts to select your Takeout folder.

Once the script has finished processing your data, it will generate an interactive HTML map that you can open in your web browser. You can then explore your location history by clicking on the markers and lines on the map.

## Example Usage

To generate a map showing your Google Location History data for the years supplied and save it to a file named "most_active_locations.html", run the following command:

python ReadMaps.py

This generates a map showing the paths between your Google Location History data for the years supplied using green lines and clusters the markers.

## Options - TO BE ADDED

The following options are not currently available when running the script but to be added:

- `--file` or `-f`: Specifies the file path to your Google Location History JSON file. If not provided, the script will prompt you to select a file using a file dialog.
- `--start-date` or `-s`: Specifies the start date (inclusive) for the data to include in the map. The date should be in YYYY-MM-DD format (e.g., "2021-01-01"). If not provided, all available data will be included.
- `--end-date` or `-e`: Specifies the end date (exclusive) for the data to include in the map. The date should be in YYYY-MM-DD format (e.g., "2022-01-01"). If not provided, all available data will be included.
- `--output-file` or `-o`: Specifies the file path for the generated HTML map. If not provided, the map will be saved to a file named "map.html" in the current directory.
- `--include-path` or `-p`: Specifies whether to include the paths between locations in the map. By default, only the locations will be shown as markers. If this option is provided, lines will be drawn between the locations to show the path taken.
- `--path-color` or `-c`: Specifies the color to use for the paths between locations. The color should be specified in hex format (e.g., "#ff0000" for red). If not provided, the color will default to blue (#3388ff).
- `--cluster-markers` or `-m`: Specifies whether to cluster the markers on the map. By default, markers will not be clustered. If this option is provided, markers that are close together will be combined into a single marker with a number indicating the number of markers it represents.
