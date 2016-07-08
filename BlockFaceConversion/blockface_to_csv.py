# converter for working with a group of input text files

import time
import csv
import operator
import os

# start time
begin_time = time.clock()

# file names and paths
code_key = "code.csv" 	# must be a csv
out_table = "block_out.csv"	# must be a csv
block_dir = "btxt"


block_files = []
for root, dirs, files in os.walk(block_dir):
    for file in files:
        if file.endswith(".txt"):
			fp = (os.path.join(root, file))
			block_files.append(fp)


# can use different file types, just make sure python can read them properly

# set up csv writer to output table
writer = csv.writer(open(out_table, 'a'),lineterminator = '\n')

# code table format:
# (name string,start int,end int)

# convert code table to custom dictionary and write header to out table
code_dict = {}
with open(code_key, 'rb') as csvfile:
	# read table
	codecsv = csv.reader(csvfile, delimiter=',')
	# set header list
	header = []
	for code in codecsv:
		# append code name to header list
		header.append(code[0])
		# calculate code length
		code_length = 1 + (int(code[2]) - int(code[1]))
		# generate code dictionary in form
		# (name,[start int, end int, length])
		code_dict[code[0]] = [int(code[1]), int(code[2]), code_length]
	# append a field name for any trailing chars not picked up by the code table
	header.append("XTRA_CHARS")
	# write header list to the out csv table
	writer.writerow(header)
# sort code_dict by initial order
code_dict = sorted(code_dict.items(), key=operator.itemgetter(1))

# print the code dictionary if you want
print code_dict

c = 0
# loop through lines (i.e. strips) and output to csv with code_dict
for cma in block_files:
	text_file = open(cma, "r")
	strips = text_file.readlines()
	num_strips =  len(strips)
	count = 0
	for strip in strips:
		# set loop length
		iter = len(code_dict)
		d = 0
		# loop through code dictionary, copying chars based on code dictionary
		row = []
		while (d < iter):
			key = code_dict[d][1]
			start_val = key[0] - 1
			end_val = start_val + key[2]
			write_val = strip[start_val:end_val]
			row.append(write_val)
			d = d + 1
		# append any trailing chars that don't have an associated code
		trailer = strip[end_val:]
		row.append(trailer)

		# write row to csv output table
		writer.writerow(row)
		count = count + 1
	c += 1

print "---------------------"
print "number of rows written"
print c

# print time
print "---------------------"
end_time = time.clock()
seconds = (end_time - begin_time)
minutes = seconds / 60
print seconds
print "seconds"
print "=============="
print minutes
