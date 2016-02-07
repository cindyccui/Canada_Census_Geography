###Geography Tape File Converter

The scripts in this repository read Statistics Canada geography tape files and converts them into readable tables and point files for GIS analysis.

Tape files are essentially text files where each information for each feature is included in each row, while the order of the characters

In census geography tape files, each row pertains to an Enumeration Area.  These are small areas, composed of one or more neighbouring blocks, and are typically the lowest level in which census data is available for analysis.

Snippet of a geography tape file:

![alt_text](img/img_tape.png)

The script tape_to_csv.py converts this tape file (.txt) into a readable table (.csv) using a record layout table.

Output csv table:

![alt_text](img/img_csv.png)

This .csv table can then be converted into a point Shapefile (.shp) with ogr2ogr.  If coordinates are given in UTM, then the "tape_csv_to_csv_by_utm.py" script will split the table by utm zone.  Then, the "ogr_utm_csv_to_shps.sh" and "shp_merge_ogr.py" scripts can be used to create a single, full coverage, point Shapefile.  

Output points on a map with Enumeration Area (black) & Census Tract (red) boundaries

![alt_text](img/img_map.png)

These scripts can be strung together as one, but were left separate so data could be checked at different points during the process.  The scripts can also be altered to allow for different input or output projections or data file types as required.  They can also be altered to read other forms of tape files.
