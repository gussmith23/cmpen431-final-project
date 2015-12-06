import re
import sys
import os

base_dir = str(sys.argv[1])
output_to_parse_dir = str(sys.argv[2])
fields_to_parse_file = str(sys.argv[3])

if not base_dir or not output_to_parse_dir or not fields_to_parse_file:
	sys.exit(-1)

# Create needed regex parsers.
value_parser = re.compile("[0-9.]+")
pattern_dict = {}
with open(base_dir + "/" + fields_to_parse_file) as file1:
    for line in file1:
    	
    	field = line.rstrip()
	pattern_dict[field] = re.compile(re.escape(field))
    	#patterns = "|".join(re.escape(line.rstrip()) for line in file1)

fields = [line.rstrip() for line in open(base_dir + "/" + fields_to_parse_file)]

print "machine,"  + ",".join(str(field) for field in fields)

#regexp = re.compile(patterns)
for file_to_parse in os.listdir(base_dir + "/" + output_to_parse_dir):
	with open(base_dir + "/" + output_to_parse_dir + "/" + file_to_parse) as file2:
		# Note: major assumption here is that we'll find each item in the same place
		#	in each file. i.e. sim_otal_insn will be at line x in ne output,
		#	and will be at line x in a different output file also.
		
		return_string = str(file_to_parse)

		lines = [line.rstrip() for line in file2]
		
		for field in fields:
			result = filter(lambda line: field in line, lines)[0]
			num = value_parser.search(result).group().strip()
			return_string += "," + num

		print return_string
