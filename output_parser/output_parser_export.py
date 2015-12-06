import re
import sys
import os


# example lines: lines = [line.rstrip() for line in open("file.txt")]
# example fields: fields = [line.rstrip() for line in open(base_dir + "/" + fields_to_parse_file)] 
def parse_output(lines, fields):
	
	# The return is a .csv in string format.
	return_string = "machine,"  + ",".join(str(field) for field in fields) + ",clock cycle,execution time\n"

	# Create needed regex parsers.
	value_parser = re.compile("[0-9.]+|true|false")

	# These are the basic fields that we MUST have. additional fields can be in fields list.
	if "issue:width" not in fields: fields.append("issue:width")
	if "issue:inorder" not in fields: fields.append("issue:inorder")
	if "sim_total_insn" not in fields: fields.append("sim_total_insn")
	if "sim_IPC" not in fields: fields.append("sim_IPC")
	
	# Important variables to log as we parse through the output.
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

	return return_string
