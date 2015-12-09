import os
import subprocess
import sys
import shlex
from os.path import isfile, join
import csv

def simulation_runner(base_dir, cfg_dir, dest_dir):

	if not base_dir or not cfg_dir or not dest_dir:
		sys.exit(-1)

	# this is messy: import parse_output.
	#execfile(base_dir + "/output_parser/output_parser_export.py")

	# a combination of base and an entry from benchmark_commands creates a command-line 
	#	command for running a simplesim benchmark.
	BASE = "/home/software/simplesim/simplesim-3.0/sim-outorder"
	benchmark_commands = {
		"bzip2": " -config {config_file} {base}/bzip2/bzip2_base.i386-m32-gcc42-nn {base}/bzip2/dryer.jpg",
		"hmmer": " -config {config_file} {base}/hmmer/hmmer_base.i386-m32-gcc42-nn {base}/hmmer/bombesin.hmm",
		"mcf": " -config {config_file} {base}/mcf/mcf_base.i386-m32-gcc42-nn {base}/mcf/inp.in",
		"sjeng": " -config {config_file} {base}/sjeng/sjeng_base.i386-m32-gcc42-nn {base}/sjeng/test.txt",
		"milc": " -config {config_file} {base}/milc/milc_base.i386-m32-gcc42-nn < {base}/milc/su3imp.in",	
		"equake": " -config {config_file} {base}/equake/equake_base.pisa_little < {base}/equake/inp.in"
	}

	# make output dir...
	if not os.path.isdir(base_dir + "/" + dest_dir):
		os.mkdir(base_dir + "/" + dest_dir)

	# get the files in the immediate directory.
	onlyfiles = [f for f in os.listdir(base_dir + "/" + cfg_dir) if isfile(join(base_dir + "/" + cfg_dir, f))]

	# Extra fields/settings to return.
	fields = []
	settings = [	"issue:inorder", 
			"issue:width",
			"bpred ", #keep space where it is
			"bpred:ras",
			"bpred:btb",
			"decode:width",
			"ruu:size",    
                        "lsq:size", 
                        "cache:dl1",  
                        "cache:dl1lat",
                        "cache:dl2",
                        "cache:dl2lat",
			"cache:il1",
                        "cache:il1lat",
                        "cache:il2",
			"cache:il2lat",
			]

	# the .csv containing info from all cfgs.
	all_cfgs_out_string = ""

	# 
	all_parsed_outputs = []
	sim_list = []

	for config_to_run in onlyfiles:
		
		# Print
		print 'Running config {0}:'.format(config_to_run)
		
		# the .csv containing info for this config.
		out_string = ""
		out_string += config_to_run + "\n"

		# collect float and int execution times so we can calculate geometric means.
		int_exec_time = []
		float_exec_time = []
	
		# The name of the folder where we'll store an output for each benchmarks
		output_folder_name = os.path.splitext( os.path.basename(config_to_run) )[0]
	
		# We only want to print the header once.
		print_column_names = 1

		sim_list_entry = {}
		sim_list_entry['config'] = config_to_run

		for benchmark_name in benchmark_commands:
			
			# Print benchmark name.
			out_string += "\n" + benchmark_name + "\n"

			# The command which will run the sim.
			command = BASE + benchmark_commands[benchmark_name]
			command = command.replace("{config_file}", base_dir + "/" + cfg_dir + "/" + str(config_to_run))
			command = command.replace("{base}", base_dir);

			# Run.
			args = shlex.split(command)
			if '<' in args:
				f_name = args[-1]
				args = args[:-2]
				p = subprocess.Popen(args, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=open(f_name))
			else:
				p = subprocess.Popen(args, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

			# Get output
			cmd_out, cmd_err = p.communicate()
			lines = cmd_err.split('\n')
			
			
			# Parse output into a dict.
			parsed_output = parse_output(lines, fields+settings)
			
			# append sim name.
			parsed_output['benchmark'] = benchmark_name 

			# store parsed output.
			all_parsed_outputs.append(parsed_output)

			# Get exec time.
			if benchmark_name in ["bzip", "hmmer", "sjeng", "mcf"]: 
				int_exec_time.append(parsed_output['execution_time'])
			else:	
				float_exec_time.append(parsed_output['execution_time'])
				
			# Print out columns.

			# First, print column name if needed.
			if print_column_names == 1:
				for column_name in parsed_output:
					out_string += column_name + ","
				out_string += "\n"

			# Then, print column values.
			for column_name in parsed_output:
				out_string += str( parsed_output[column_name] ) + ","
			out_string += "\n"

			print '\t{0} execution time: {1}'.format(benchmark_name, parsed_output['execution_time'])

			# We shouldn't do this every iteration of this loop; we only need to do it once.
			for setting in settings:
				sim_list_entry[setting] = parsed_output[setting]

		int_exec_time_mean = (reduce(lambda x, y: x*y, int_exec_time))**(1.0/len(int_exec_time)) 
		float_exec_time_mean = (reduce(lambda x, y: x*y, float_exec_time))**(1.0/len(float_exec_time)) 
	
		sim_list_entry['int_exec_time'] = int_exec_time_mean
		sim_list_entry['float_exec_time'] = float_exec_time_mean

		# Log.
		print 'mean int exec time:\t{0}'.format(int_exec_time_mean)
		print 'mean float exec time:\t{0}'.format(float_exec_time_mean)
		print

		out_string += "\n" + str(int_exec_time_mean) + "\n" + str(float_exec_time_mean) + "\n"

		# Append this cfg run output to the total .csv.
		all_cfgs_out_string += str(out_string) + "\n"

		# Write this cfg's output to file.
		f = open(base_dir + "/" + dest_dir + "/" + config_to_run[:32] + ".csv", "w")
		f.write(out_string)
		
		# append to the sim list.
		sim_list.append(sim_list_entry)


	# write to file.
	f = open(base_dir + "/" + dest_dir + "/" + "out.csv", 'a')
	f.write(all_cfgs_out_string)

	# Sort output.
	all_parsed_outputs = sorted(all_parsed_outputs, key=lambda k: k['execution_time'])

	with open(base_dir + "/" + dest_dir + "/" + 'all.csv', 'wb') as output_file:
		keys = sim_list[0].keys()

		header = {}
		for key in keys:
			header[key] = str(key)
		sim_list.insert(0, header)

		dict_writer = csv.DictWriter(output_file, keys)
		dict_writer.writerows(sim_list)

