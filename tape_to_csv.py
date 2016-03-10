import time
import csv
import operator
import os

# start time
begin_time = time.clock()

# file names and paths
code_key = "code.csv" 	# must be a csv
tape_file = "gtf76.txt"	# must be a txt
out_table = "out.csv"	# must be a csv
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

# set up reading the tape file
text_file = open(tape_file, "r")
strips = text_file.readlines()
num_strips =  len(strips)

# loop through lines (i.e. strips) and output to csv with code_dict
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

print "---------------------"
print "number of rows written"
print count

# print time
print "---------------------"
end_time = time.clock()
seconds = (end_time - begin_time)
minutes = seconds / 60
print seconds
print "seconds"
print "=============="
print minutes
print "minutes"
