import os
import subprocess
import sys
import shlex
from os.path import isfile, join

# Arguments
base_dir = str(sys.argv[1])
cfg_dir = str(sys.argv[2])
dest_dir = str(sys.argv[3])

if not base_dir or not cfg_dir or not dest_dir:
	sys.exit(-1)

# this is messy: import parse_output.
execfile(base_dir + "/output_parser/output_parser_export.py")

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
os.mkdir(base_dir + "/" + dest_dir)

# get the files in the immediate directory.
onlyfiles = [f for f in os.listdir(base_dir + "/" + cfg_dir) if isfile(join(base_dir + "/" + cfg_dir, f))]


# Extra fields to return.
fields = []

# For each config, we'll generate 6 outputs.
for config_to_run in onlyfiles:

	# collect float and int execution times so we can calculate geometric means.
	int_exec_time = []
	float_exec_time = []

	# The name of the folder where we'll store an output for each benchmarks
	output_folder_name = os.path.splitext( os.path.basename(config_to_run) )[0]
	
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
		parsed_output = parse_output(lines, fields)

		# Get exec time.
		if benchmark_name in ["bzip", "hmmer", "sjeng", "mcf"]: 
			int_exec_time.append(parsed_output['execution_time'])
		else:	
			float_exec_time.append(parsed_output['execution_time'])
	
	
	int_exec_time_mean = (reduce(lambda x, y: x*y, int_exec_time))**(1.0/len(int_exec_time)) 
	float_exec_time_mean = (reduce(lambda x, y: x*y, float_exec_time))**(1.0/len(float_exec_time)) 

	print int_exec_time_mean
	print float_exec_time_mean
