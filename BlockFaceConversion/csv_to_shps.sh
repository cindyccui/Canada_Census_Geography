# creates point shapefiles for csv tables with different utm projections
# requires gdal/ogr
# utm epsg should be in file name from csv_to_csv_by_utm.py

# Jeff Allen
# jeff.allen@mail.utoronto.ca

cd csv_by_utm_zone
for i in *
do
	echo "----------------------------"
	echo "$i"
	f="${i%.*}"
	n="${f:3}"
	echo "$f"
	echo "$n"
	ogr2ogr "$f".shp -t_srs "EPSG:4269" "$f".csv -dialect sqlite -sql "SELECT MakePoint(CAST(utm_x as REAL), CAST(utm_y as REAL), "$n") Geometry, * FROM "$f""
done
echo "----------------------------"

# excerpt for just one table conversion:

# ogr2ogr "$f".shp -t_srs "EPSG:4269" "$f".csv -dialect sqlite -sql "SELECT MakePoint(CAST(utm_x as REAL), CAST(utm_y as REAL), "$n") Geometry, * FROM "$f""

# or using a .vrt file:

# ogr2ogr -f "ESRI Shapefile" . gaf.csv && ogr2ogr -f "ESRI Shapefile" . gaf.vrt
