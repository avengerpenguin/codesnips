```python
import pandas as pd
import geopandas as gpd  

# Read CSV with columns "lon" and "lat" as floats
df = pd.read_csv('my-csev.csv')
df = gpd.GeoDataFrame(
    df, geometry=gpd.points_from_xy(df.lon, df.lat), crs="EPSG:4326"  
)
# Optionally (saves memory) drop original lat/lon columns
df.drop('lon', axis=1, inplace=True)  
df.drop('lat', axis=1, inplace=True)  
```

See also [[Using GeoPandas to group points into lines or paths]]