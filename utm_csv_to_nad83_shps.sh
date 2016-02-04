# creates point files for csv tables with different utm projections

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
