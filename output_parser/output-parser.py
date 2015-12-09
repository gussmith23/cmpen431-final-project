import re
import sys
import os

base_dir = str(sys.argv[1])
output_to_parse_dir = str(sys.argv[2])
fields_to_parse_file = str(sys.argv[3])

if not base_dir or not output_to_parse_dir or not fields_to_parse_file:
	sys.exit(-1)

# Create needed regex parsers.
value_parser = re.compile("[0-9.]+|true|false")
#bool_parser  = re.compile("[true|false]+")

fields = [line.rstrip() for line in open(base_dir + "/" + fields_to_parse_file)] 
if "issue:width" not in fields: fields.append("issue:width")
if "issue:inorder" not in fields: fields.append("issue:inorder")
if "sim_total_insn" not in fields: fields.append("sim_total_insn")
if "sim_IPC" not in fields: fields.append("sim_IPC")


print "machine,"  + ",".join(str(field) for field in fields) + ",clock cycle,execution time"

#regexp = re.compile(patterns)
for file_to_parse in os.listdir(base_dir + "/" + output_to_parse_dir):
	with open(base_dir + "/" + output_to_parse_dir + "/" + file_to_parse) as file2:
		# Note: major assumption here is that we'll find each item in the same place
		#	in each file. i.e. sim_otal_insn will be at line x in ne output,
		#	and will be at line x in a different output file also.
		
		# column 1: machine name (== filename)
		return_string = str(file_to_parse)

		lines = [line.rstrip() for line in file2]
		
		#
		width = 0
		inorder = 0
		ipc = 0
		total_insn = 0
		clock_cycle = 0

		for field in fields:
			result = filter(lambda line: field in line, lines)[0]
			val = value_parser.search(result).group().strip()
			return_string += "," + str(val)
			
			# Keep track of the vals needed to calculate clock cycle.
			if field == "issue:width": width = int(val)
			if field == "issue:inorder":
				if val == "true": inorder = True
				else: inorder = False
			if field == "sim_IPC": ipc = float(val)
			if field == "sim_total_insn": total_insn = int(val)
		
		
		# Lookup clock cycle.
		if inorder == True:	# static
			if width == 1: clock_cycle = 100e-12
			if width == 2: clock_cycle = 115e-12
			if width == 3: clock_cycle = 130e-12
			if width == 4: clock_cycle = 145e-12
		else:
			if width == 2: clock_cycle = 125e-12
			if width == 4: clock_cycle = 160e-12
			if width == 8: clock_cycle = 195e-12
		
		# second to last column: clock cycle. 
		return_string += "," + str(clock_cycle)

		# last column: execution time
		execution_time = (total_insn * clock_cycle)/ipc
		return_string += "," + str(execution_time)

		print return_string
