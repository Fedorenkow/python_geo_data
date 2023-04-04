import rasterio
import geopandas as gpd


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

clay = find_soil(pointX, pointY, "./soil_data/clay.tif")
sand = find_soil(pointX, pointY, "./soil_data/sand.tif")
density = find_soil(pointX, pointY, "./soil_data/density.tif")
soil_moisture = find_soil(pointX, pointY, "soil_moisture.tif")