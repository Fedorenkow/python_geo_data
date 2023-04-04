import rasterio
import geopandas as gpd
from shapely import Point


def find_point(point):
    gdf = gpd.read_file("field_centroids.geojson")
    point = gdf.geometry.iloc[point]
    x, y = point.x, point.y
    return x, y


def find_soil(x, y, raster_file):
    with rasterio.open(raster_file) as src:
        row, col = src.index(x, y)
        soil_val = src.read(1, window=((row, row + 1), (col, col + 1)))
        print(f"{raster_file} content at point ({x},{y}): {soil_val[0][0]}")
        return soil_val


pointX, pointY = find_point(0)

ball = Point(pointX, pointY)

clay = find_soil(pointX, pointY, "./soil_data/clay.tif")[0][0]
sand = find_soil(pointX, pointY, "./soil_data/sand.tif")[0][0]
density = find_soil(pointX, pointY, "./soil_data/density.tif")[0][0]
soil_moisture = find_soil(pointX, pointY, "soil_moisture.tif")[0][0]

data_soil = {
    "clay": clay,
    "sand": sand,
    "density": density,
    "soil_moisture": soil_moisture}

soils = gpd.GeoDataFrame([data_soil], geometry=[ball])
soils.to_file("output.geojson", driver="GeoJSON")
