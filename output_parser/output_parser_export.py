import re
import sys
import os


# example lines: lines = [line.rstrip() for line in open("file.txt")]
# example fields: fields = [line.rstrip() for line in open(base_dir + "/" + fields_to_parse_file)] 
def parse_output(lines, fields):

	if len(lines) < 1:
		print "parse_output error: no lines passed!"
		return None

	# Return
	return_dict = {}

	# Create needed regex parsers.
	value_parser = re.compile("[0-9.]+|true|false|bimod|2lev")
	cache_parser = re.compile("[0-9]+:[0-9]+:[0-9]+:[a-z]+")
	bpred_parser = re.compile("bimod|2lev")

	# These are the basic fields that we MUST have. additional fields can be in fields list.
	if "issue:width" not in fields: fields.append("issue:width")
	if "issue:inorder" not in fields: fields.append("issue:inorder")
	if "sim_total_insn" not in fields: fields.append("sim_total_insn")
	if "sim_IPC" not in fields: fields.append("sim_IPC")
	
	# The return is a .csv in string format.
	# Generate column header
	return_string = "machine" 
	for field in fields: return_string += "," + field
	return_string += ",clock cycle,execution time\n"

	# include machine name in return val
	return_string += ", PLACEHOLDER"
	return_dict['name'] = "PLACEHOLDER"

	# Important variables to log as we parse through the output.
	width = 0
	inorder = 0
	ipc = 0
	total_insn = 0
	clock_cycle = 0

	for field in fields:
		
		result = filter(lambda line: field in line, lines)[0]
		
		# parse value out.
		if field == "cache:dl1" or field == "cache:dl2" or field == "cache:il1" or field == "cache:il2":
			val = cache_parser.search(result)
			if val is not None:
				val = val.group().strip()
			else:
				val = "not found"
		elif field == "bpred ": #note the space.
			val = bpred_parser.search(result).group().strip()
		else:
			val = value_parser.search(result).group().strip()
		
		# put the value in our return val.
		return_string += "," + str(val)
		return_dict[field] = val

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
	return_dict['clock_cycle'] = clock_cycle

	# last column: execution time
	execution_time = (total_insn * clock_cycle)/ipc
	return_string += "," + str(execution_time)
	return_dict['execution_time'] = execution_time

	return return_dict
