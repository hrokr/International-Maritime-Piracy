import geopandas as gpd

# Load your geodatabase
gdb_path = "../data/Asam_data_download.gdb"

# List all tables in the geodatabase
gdf = gpd.read_file(gdb_path)
print(gdf)


print(gdf.info())

print(gdf["geometry"][:10])

# This will list all tables and feature classes
