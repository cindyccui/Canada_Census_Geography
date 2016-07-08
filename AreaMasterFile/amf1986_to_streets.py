# this mediocre script creates street geojson geometry from 1986 Area Master Files

# Jeff Allen
# jeff.allen@mail.utoronto.ca

# needs to run next to a folder with the amf .txt Files,
# pre set up output folders for geojson destinations,
# and with gdal/ogr installed

import csv
import os
import json
import copy
from subprocess import call
import time

start_time = time.time()

folder = "amf86"
slash = "//"

# headers of each row for reference
mun_header = [
	'metro_code',
	'munic_code',
	'seq_code',
	'munic_name'
]
feat_header = [
	'metro_code',
	'munic_code',
	'feat_code',
	'seq_num',
	'feat_type',
	'sub_f_type',
	'sect_num',
	'cent_check',
	'feat_name',
	'str_type',
	'feat_dir'
]
point_header = [
	'metro_code',
	'munic_code',
	'feat_code',
	'seq_num',
	'feat_type',
	'sub_f_type',
	'sect_num',
	'cent_check',
	'node_num',
	'node_type',
	'node_x_utm',
	'node_y_utm'
]
street_header = [
	'metro_code',
	'munic_code',
	'feat_code',
	'seq_num',
	'feat_type',
	'sub_f_type',
	'sect_num',
	'cent_check',
	'node_num',
	'node_type',
	'node_x_utm',
	'node_y_utm',
	'add_b_le',
	'add_b_ri',
	'add_a_le',
	'add_a_ri',
	'cent_le_x',
	'cent_le_y',
	'cen_ri_x',
	'cen_ri_y',
	'xref_munco',
	'xref_ftco',
	'xref_seqn',
	'xref_ft_n',
	'xref_st_ty'
]

amf_count = 0
for root, dirs, files in os.walk(folder):
    for amffile in files:
        if amffile.endswith(".txt"):
			print amffile
			amf_count += 1

			line_count = 0

			feat_store = []
			mun_store = []
			point_store = []
			street_store = []
			jerk_store = []

			amf_text_file = amffile
			text = open(folder + slash + amf_text_file, "r")
			lines = text.readlines()

			c = m = f = p = s = j = 0

			line_types = [] # h, m, f, p, s, a

			# syntax reader for amf text files
			for line in lines:

				line_count += 1

				#top header record
				if line == lines[0]:

					utm = int(line[35:38]) #utm zone

					# there's more stuff in here to parse

					line_types.append('h')

				# municipality stuff
				elif line[10:14] == "    " and line != lines[0]:
					print "------------------"
					mun_data = []
					mun_data.append(line[0:4]) # metro area code
					mun_data.append(line[4:8]) # municipality code
					mun_data.append(line[14:17]) # sequence number
					mun_name = line[21:42].rstrip() # municipality name
					mun_data.append(mun_name)
					mun_store.append(mun_data)
					m += 1
					line_types.append('m')

				# feature headers (eg roads, rivers)
				elif line[14:17] == '000':
					feat_data = []
					feat_data.append(line[0:4]) # metro area code
					feat_data.append(line[4:8]) # municipality code
					feat_data.append(line[8:14]) # feature code
					feat_data.append(line[14:17]) # sequence code
					feat_data.append(line[17:18]) # feat type
					feat_data.append(line[18:19]) # sub-feat type
					feat_data.append(line[19:21]) # section number '00'
					feat_data.append(line[24:26]) # centroid calculation check
					feat_name = line[26:46].rstrip() # feature name
					feat_data.append(feat_name)
					feat_data.append(line[46:48]) # street type
					feat_data.append(line[48:50]) # feature direction
					feat_store.append(feat_data)
					f += 1
					line_types.append('f')

				# point records
				elif line[17:18] == 'P':
					point_data = []
					point_data.append(line[0:4]) # metro area code
					point_data.append(line[4:8]) # municipality code
					point_data.append(line[8:14]) # feature code
					point_data.append(line[14:17]) # sequence number
					point_data.append(line[17:18]) # feat type
					point_data.append(line[18:19]) # sub-feat tyep
					point_data.append(line[19:21]) # section number
					point_data.append(line[24:26]) # centroid calculation check
					point_data.append(line[26:30]) # node number
					point_data.append(line[30:31]) # node type
					point_data.append(line[31:37]) # node utm x
					point_data.append(line[37:44]) # node utm x
					point_store.append(point_data)
					p += 1
					line_types.append('p')

				# street records
				elif len(line) > 72 and line[17:18] != 'D':
					street_data = []
					street_data.append(line[0:4]) # metro area code
					street_data.append(line[4:8]) # municipality code
					street_data.append(line[8:14]) # feature code
					street_data.append(line[14:17]) # sequence number
					street_data.append(line[17:18]) # feat type
					street_data.append(line[18:19]) # sub-feat tyep
					street_data.append(line[19:21]) # section number
					street_data.append(line[24:26]) # centroid calculation check
					street_data.append(line[26:30])	# node number
					street_data.append(line[30:31]) # node type
					street_data.append(line[31:37]) # node utm x
					street_data.append(line[37:44]) # node utm y
					street_data.append(line[44:49]) # address before left
					street_data.append(line[49:54]) # address before right
					street_data.append(line[54:59]) # address after left
					street_data.append(line[59:64]) # address after right
					street_data.append(line[64:70]) # centroid left x
					street_data.append(line[70:77]) # centroid left y
					street_data.append(line[77:83]) # centroid right x
					street_data.append(line[83:90]) # centroid right y
					street_data.append(line[90:94]) # xref municipality code
					street_data.append(line[94:100]) # xref feature code
					street_data.append(line[100:103]) # xref sequence number
					street_data.append(line[103:108]) # xref feature name
					street_data.append(line[108:110]) # xref street type
					street_store.append(street_data)
					s += 1
					line_types.append('s')

				# alias features
				else:
					jerk_store.append(line)
					j += 1
					line_types.append('a')

				c += 1

			print "------------------"
			print utm
			print "------------------"
			print m, f, p, s, j, c
			print "------------------"
			print len(line_types)

			feature_schema = {
				"type":"Feature",
				"geometry":{
					"type":"LineString",
					"coordinates":[]
				},
				"properties": {
				}
			}


			# writing data to geojson features

			pre_fc = 0
			fc = 0
			feat_list = []
			feats_for_geo = []

			even_fr_add = -1
			odd_fr_add = -1

			for street in street_store:
				now_coord = [int(street[10]),int(street[11])]
				if street[9] != "B":
					fc += 1

					linestring = []
					feat = {}
					linestring = [now_coord, pre_coord]
					feat = feature_schema
					feat["geometry"]["coordinates"] = []
					feat["geometry"]["coordinates"].append(linestring[0])
					feat["geometry"]["coordinates"].append(linestring[1])

					for feature in feat_store:
						if street[2] == feature[2]:
							street_name = feature[8]
							street_type = feature[9]
							street_dir = feature[10]
							break

					for municip in mun_store:
						if street[1] == municip[1]:
							municip_name = municip[3]
							break

					feat["properties"]["munic_name"] = municip_name
					feat["properties"]["feat_name"] = street_name
					feat["properties"]["ft_str_type"] = street_type
					feat["properties"]["ft_str_dir"] = street_dir

					ss = 0
					while ss < 12:
						prop = street_header[ss]
						feat["properties"][prop] = street[ss]
						ss += 1


					# feat["properties"]["metro_area"] = street[0]



					street_data.append(line[0:4]) # metro area code
					street_data.append(line[4:8]) # municipality code
					street_data.append(line[8:14]) # feature code
					street_data.append(line[14:17]) # sequence number
					street_data.append(line[17:18]) # feat type
					street_data.append(line[18:19]) # sub-feat tyep
					street_data.append(line[19:21]) # section number
					street_data.append(line[24:26]) # centroid calculation check
					street_data.append(line[26:30])	# node number
					street_data.append(line[30:31]) # node type
					street_data.append(line[31:37]) # node utm x
					street_data.append(line[37:44]) # node utm y

					feat["properties"]["a_even_fr"] = even_fr_add
					feat["properties"]["a_odd_fr"] = odd_fr_add

					even_to_add = -1
					odd_to_add = -1

					l_add = -1
					r_add = -1

					try:
						l_add = int(street[12])
						if l_add % 2 == 0:
							even_to_add = l_add
						if l_add % 2 != 0:
							odd_to_add = l_add
					except:
						l_add = -1

					try:
						r_add = int(street[13])
						if r_add % 2 == 0:
							even_to_add = r_add
						if r_add % 2 != 0:
							odd_to_add = r_add
					except:
						r_add = -1

					feat["properties"]["a_even_to"] = even_to_add
					feat["properties"]["a_odd_to"] = odd_to_add

					i = 0

					feat_list.append(copy.deepcopy(feat))

				even_fr_add = -1
				odd_fr_add = -1

				l_add = -1
				r_add = -1

				try:
					l_add = int(street[14])
					if l_add % 2 == 0:
						even_fr_add = l_add
					if l_add % 2 != 0:
						odd_fr_add = l_add
				except:
					l_add = -1

				try:
					r_add = int(street[15])
					if r_add % 2 == 0:
						even_fr_add = r_add
					if r_add % 2 != 0:
						odd_fr_add = r_add
				except:
					r_add = -1

				pre_fc = (street[2])
				# pre_add = [street(12),street(13),street(14),street(15)]
				pre_coord = [int(street[10]),int(street[11])]

			print fc
			print s
			print f
			print p
			print i

			# write geo ref info in geojson format
			epsg = str(26700 + int(utm))
			crs = ("urn:ogc:def:crs:EPSG::%s" %epsg)

			# create geojson
			geojson = {
				"type":"FeatureCollection",
				"crs": {
			    "type": "name",
			    "properties": {
			      "name": crs
			      }
			    },
				"features": feat_list
			}

			# remove stupid chars in file name
			amf_text_file = amf_text_file[:-4]
			amf_text_file = amf_text_file[4:]

			# write to geojson in folder
			with open('geojsons' + slash + amf_text_file + '.geojson', 'w') as fp:
			    json.dump(geojson, fp)

### to nad83 folder

geojsons_in_folder = "geojsons"
geojsons_out_folder = "geojsons_nad83"
slash = "//"

for root, dirs, files in os.walk(geojsons_in_folder):
    for gj in files:
        if gj.endswith(".geojson"):
            print(gj)
            call(["ogr2ogr", "-f", "GeoJSON", geojsons_out_folder + slash + "nad83_%s" %gj,"-t_srs", "EPSG:4269", geojsons_in_folder + slash + gj])

### merge them all!!! hahahahahahaha

# watch out for that memeroy error though - may need to do outside script

geojsons_in_folder = "geojsons_nad83"
out_folder = "geojsons_merge"
slash = "//"

features_list = []
for root, dirs, files in os.walk(geojsons_in_folder):
    for gj in files:
        if gj.endswith(".geojson"):
            gj_path = geojsons_in_folder + slash + gj
            print gj_path
            with open(gj_path) as data_file:
                data = json.load(data_file)
                x = data["features"]
                features_list = features_list + x

merged_geojson = {
    "type":"FeatureCollection",
    "crs": { "type": "name", "properties": { "name": "urn:ogc:def:crs:EPSG::4269" }
    },
    "features": features_list
}

with open(out_folder + slash + "streets.geojson", 'w') as fp:
    json.dump(merged_geojson, fp)


print("--- %s seconds ---" % (time.time() - start_time))
