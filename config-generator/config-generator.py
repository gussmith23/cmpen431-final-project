# Arguments:
# argv[1] - the absolute path of the final project directory. this is just for testing purposes at the moment;
#		i'm trying to avoid the headache of figuring out the intracacies of current working directories
#		when calling a bash script from a python script which itself is called from a diff. folder.
# argv[2] - the path to the configs folder RELATIVE TO the above path.

import subprocess
import sys

########################
## FUNCTIONS

# Arguments:
# _cfg_dir: configs directory relative to base of project.
# _working_set_dir: location to make new working set, relative to base of project.
def new_working_set(_cfg_dir, _working_set_dir):
	command = "sh" + " " + base_dir + "/config-generator/new-working-set.sh" + " "  + base_dir + " " + _cfg_dir + " " + _working_set_dir
	subprocess.call(command.split())

#######################
## MAIN ROUTINE

base_dir = str(sys.argv[1])
cfg_dir = str(sys.argv[2])

if not base_dir or not cfg_dir:
	sys.exit(-1)

new_working_set(cfg_dir,cfg_dir+"/pythtest")

	
