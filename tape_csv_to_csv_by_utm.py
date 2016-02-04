import csv
import os
import time
from subprocess import call
import sys
from osgeo import ogr

begin_time = time.clock()

#input table
in_table = "out.csv"
in_tape_table = open(in_table)

#names of utm fields
utm_field = "utmzone"
utm_x_field = "utm_x"
utm_y_field = "utm_y"

read_table = csv.reader(in_tape_table)

# loop through first row, coding the field numbers that match the utm fields
field_count = 0
row_count = 0
for row in read_table:
	field_count = 0
	for field in row:
		if field == utm_field:
			utm_field_num = field_count
			print "utm"
		elif field == utm_x_field:
			utm_x_field_num = field_count
			print "utmX"
		elif field == utm_y_field:
			utm_y_field_num = field_count
			print "utmY"
		else:
			print "no"
		field_count += 1
	# save the header row for future coding
	header = row
	break

# print the header if you want
print "========================"
print header
print "========================"

# create a list of utm zones by looping through rows in table
utm_zone_list = []
utm_zone_count = 0
for row in read_table:
	if row[utm_field_num] not in utm_zone_list:
		utm_zone_list.append(row[utm_field_num])
		utm_zone_count += 1
	row_count += 1

# print some utm zone info if you want
print "========================"
print sorted(utm_zone_list)
print field_count
print row_count
print utm_zone_count
print "========================"

# reset csv reader
in_tape_table.close()
in_tape_table = open(in_table)
read_table = csv.reader(in_tape_table)

# create output directory
os.mkdir('csv_by_utm_zone')


# loop through utm zone list, writing any rows from input table that match this zone
total_row_count = 0
for zone in utm_zone_list:
	utm_nad83_epsg = 26900 + int(zone)
	writer = csv.writer(open("csv_by_utm_zone/utm" + str(utm_nad83_epsg) + ".csv", 'a'),lineterminator = '\n')
	writer.writerow(header)

	in_tape_table.close()
	in_tape_table = open(in_table)
	read_table = csv.reader(in_tape_table)

	count_by_zone = 0

	for row in read_table:

		if row[utm_field_num] == zone:
			writer.writerow(row)
			count_by_zone += 1


	total_row_count = total_row_count + count_by_zone


# call csv to point shell script, but
# calling this .sh doesn't seem to work properly here, running it outside does
# call(['sh','utm_csv_to_nad83_shps.sh'])

# print total row count
print "========================"
print "total row count:"
print total_row_count
print "========================"

# print time
end_time = time.clock()
seconds = (end_time - begin_time)
minutes = seconds / 60
print seconds
print "seconds"
print "========================"
print minutes
print "minutes"
