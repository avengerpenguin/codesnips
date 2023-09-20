Assumes a pandas DataFrame with a column called "geometry". See [[Using GeoPandas to create points from latitude and longitude]] to create from latitude/longitude pairs. Useful if you have a series of points many-to-many mapped to some id (`some_id` below) and the dataframe is ordered by that ID then by the order lines appear in the path.

```python
from shapely.geometry import LineString
df = df.groupby('some_id')['geometry'].apply(
	lambda x: LineString(x.tolist())
).reset_index(name='path')
```
