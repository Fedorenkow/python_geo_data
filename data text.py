import rasterio
from rasterio.features import shapes
import geopandas as gpd
from shapely.geometry import Point

with rasterio.open('./soil_moisture.tif') as src:
    image = src.read(1)
    results = (
        {'properties': {'raster_val': v}, 'geometry': s}
        for i, (s, v)
        in enumerate(shapes(image, mask=None, transform=src.transform))
    )

gdf = gpd.read_file("field_centroids.geojson")
point=gdf.geometry.iloc[0]
x = point.x,point.y
print(x)


