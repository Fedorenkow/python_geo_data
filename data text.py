import rasterio
import geopandas as gpd
from shapely import Point
import json


# Function to find coordinations from geojson
def find_point(point):
    gdf = gpd.read_file("field_centroids.geojson")
    point = gdf.geometry.iloc[point]
    x, y = point.x, point.y
    return x, y


# Function to find soil for sand etc.
def find_soil(x, y, raster_file):
    with rasterio.open(raster_file) as src:
        row, col = src.index(x, y)
        soil_val = src.read(1, window=((row, row + 1), (col, col + 1)))
        print(f"{raster_file} content at point ({x},{y}): {soil_val[0][0]}")
        return soil_val


for i in range(1, 40):
    # It's for find some need string in geojson

    with open('field_centroids.geojson') as f:
        data = json.load(f)
        first_feature = data['features'][i]

    id_json = first_feature['properties']['id']
    name_json = first_feature['properties']['Name']

    pointX, pointY = find_point(i)
    ball = Point(pointX, pointY)

    clay = int(find_soil(pointX, pointY, "./soil_data/clay.tif")[0][0])
    sand = int(find_soil(pointX, pointY, "./soil_data/sand.tif")[0][0])
    density = int(find_soil(pointX, pointY, "./soil_data/density.tif")[0][0])
    soil_moisture = int(find_soil(pointX, pointY, "soil_moisture.tif")[0][0])

    properties = {
        'id': id_json,
        'Name': name_json,
        'soil': {
            'clay': clay,
            'sand': sand,
            'density': density
        },
        'soil_moisture': soil_moisture,
        'coordinates': {
            'lat': pointX,
            'lng': pointY
        }

    }
    gdf = gpd.GeoDataFrame(data=[properties], geometry=[ball])
    gdf.to_file('result.geojson', driver='GeoJSON', newline='\n')
    with open('result.geojson', "a") as f:
        properties = {
            'id': id_json,
            'Name': name_json,
            'soil': {
                'clay': clay,
                'sand': sand,
                'density': density
            },
            'soil_moisture': soil_moisture,
            'coordinates': {
                'lat': pointX,
                'lng': pointY
            }
        }
        data["features"].append(properties)
        f.seek(0)
        json.dump(data, f)
        f.truncate()
