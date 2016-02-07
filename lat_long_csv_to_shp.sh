
ogr2ogr mr_test.shp out_91_2.csv -dialect sqlite -sql "SELECT MakePoint(CAST(lon_2 as REAL), CAST(lat_dec_deg as REAL), 4269) Geometry, * FROM out_91_2"
