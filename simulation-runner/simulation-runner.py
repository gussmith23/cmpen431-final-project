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
	# NOTE: THIS DOESN'T WORK HERE! YOU NEED TO Import parse_output 
	# before calling simulation_runner. sorry for how messy that is.
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

	# The list of results from each machine.
	sim_list = []

	# There's some setup we need to do on the first iteration (e.g. setup output .csv.)
	#	This indicates whether or not that needs to be done.
	first_iteration_setup = 1

	# This is the file where the parsed output for each machine will go.
	output_csv = open(base_dir + "/" + dest_dir + "/all_machines.csv", 'w')

	# this is the DictWriter writing into the output_csv file.
	dict_writer = 0 # initialized after first iteration.


	for config_to_run in onlyfiles:
		
		# Print
		print 'Running config {0}:'.format(config_to_run)
		
		# collect float and int execution times so we can calculate geometric means.
		int_exec_time = []
		float_exec_time = []
		
		# our entry into sim_list. thus, sim_list is a list of these objects below.
		# each sim_list_entry corresponds to a row in our output .csv.
		sim_list_entry = {}

		sim_list_entry['config'] = config_to_run

		# run all six benchmarks.
		for benchmark_name in benchmark_commands:

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

			# Get exec time.
			if benchmark_name in ["bzip", "hmmer", "sjeng", "mcf"]: 
				int_exec_time.append(parsed_output['execution_time'])
			else:	
				float_exec_time.append(parsed_output['execution_time'])
				
			print '\t{0} execution time: {1}'.format(benchmark_name, parsed_output['execution_time'])

			# We shouldn't do this every iteration of this loop; we only need to do it once.
			for setting in settings:
				sim_list_entry[setting] = parsed_output[setting]

			# For each machine, we need to keep track of milc/mcf data (so graders can check validity)
			if benchmark_name is "milc" or benchmark_name is "mcf":
				sim_list_entry[benchmark_name + "_execution_time"] = parsed_output['execution_time']
				sim_list_entry[benchmark_name + "_ipc"] = parsed_output['sim_IPC']

		# End for each benchmark.

		# Calculate and store geometric means.
		int_exec_time_mean = (reduce(lambda x, y: x*y, int_exec_time))**(1.0/len(int_exec_time)) 
		float_exec_time_mean = (reduce(lambda x, y: x*y, float_exec_time))**(1.0/len(float_exec_time)) 
		sim_list_entry['int_exec_time'] = int_exec_time_mean
		sim_list_entry['float_exec_time'] = float_exec_time_mean

		# Log.
		print 'mean int exec time:\t{0}'.format(int_exec_time_mean)
		print 'mean float exec time:\t{0}'.format(float_exec_time_mean)
		print

		# If this is the first cfg, open up .csv for writing and append header.
		if first_iteration_setup == 1:
			
			# Open dict writer
			keys = sim_list_entry.keys()
			dict_writer = csv.DictWriter(output_csv, keys)

			# Create .csv header.
			header = {}
			for key in keys:
				header[key] = str(key)
			sim_list.insert(0, header)
			
			# Write header.
			dict_writer.writerow(header)

			first_iteration_setup = 0
		
		# append to the sim list.
		sim_list.append(sim_list_entry)

		# writerow to .csv.
		dict_writer.writerow(sim_list_entry)
