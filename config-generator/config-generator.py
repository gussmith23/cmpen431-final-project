# Config Generation Script
# 
# Author: Gus Smith <hfs5022@psu.edu>
#
# Arguments:
# argv[1] - the absolute path of the final project directory. this is just for testing purposes at the moment;
#		i'm trying to avoid the headache of figuring out the intracacies of current working directories
#		when calling a bash script from a python script which itself is called from a diff. folder.
# argv[2] - the path to the configs folder RELATIVE TO the above path.

import subprocess
import sys
import os


#######################
## Fields

# These keys are used to lookup a string which is then passed
#	to sed for find-and-replace.
# The values should each map to a single line; i.e., if we use this
#	dictionary to find-and-replace a setting, we won't overwrite
#	multiple lines.
simplesim_settings = {
	ifqsize: 	"-fetch:ifqsize",
	fspeed: 	"-fetch:speed",
	fmplat:		"-fetch:mplat",
	bpred:		"-bpred ",		# This one may be an issue...
	ras:		"-bpred:ras",
	dwidth:		"-decode:width",
	iwidth:		"-issue:width",
	inorder:	"-issue:inorder",
	wrongpath:	"-issue:wrongpath",
	ruusize:	"-ruu:size",
	lsqsize:	"-lsq:size",
	ialu:		"-res:ialu",
	imult:		"-res:imult",
	fpalu:		"-res:fpalu",
	fpmult:		"-res:fpmult",
	memport:	"-res:memport",
	il1:		"-cache:il1 ",
	il2:		"-cache:il2 ",
	dl1:		"-cache:dl1 ",
	dl2:		"-cache:dl2 ",
	itlb:		"-tlb:itlb",
	dtlb:		"-tbl:dtlb",
	il1lat:		"-cache:il1lat",
	il2lat:		"-cache:il2lat",
	dl1lat:		"-cache:dl1lat",
	dl2lat:		"-cache:dl2lat",
	memlat:		"-mem:lat",
	memwidth:	"-mem:width",
	redir:		"-redir:sim"
}


########################
## FUNCTIONS


## BASH SCRIPT WRAPPERS
# new_working_set, modify_working_set, merge_working_set
# These functions wrap scripts which modify the filesystem directly.
# These scripts create "working sets" - groups of configs that are all modified
# together. practically, this allows us to create a new working set (which will
# copy all existing configs to a new location), modify the working set (which
# changes the same setting in all configs), and merge the working set (which dumps
# the new configs back into the old config directory). The result is that we
# will have doubled the number of configs, each new config being the same as
# an old config plus one single settings change (done in the modify working 
# set step).


# new_working_set
#	Wrapper for new-working-set.sh, which generates a new "working set"; i.e.
#	copies all .cfgs from _cfg_dir into _working_set_dir with new random names.
#
# Arguments:
# _cfg_dir: configs directory relative to base of project.
# _working_set_dir: location to make new working set, relative to base of project.

def new_working_set(_cfg_dir, _working_set_dir):
	command = "sh" + " " + base_dir + "/config-generator/new-working-set.sh" + " "  + base_dir + " " + _cfg_dir + " " + _working_set_dir
	subprocess.call(command.split())


# modify_working_set
#	Wrapper for modify-working-set.sh, which modifes the working set with
#	some attribute change.
#
# Arguments:
# _working_set_dir - the working set, relative to base of project.
# regexps - an array of strings which will be passed to sed. for example,
#		'/find me/c\\newstring' replaces lines containing "findme" with
#		"newstring". Note the double backslash - it is technically
#		just a single backslash, but it needs to be escaped in python.

def modify_working_set(_working_set_dir, regexps):
	command = "sh" + " " + base_dir + "/config-generator/modify-working-set.sh" + " "  + base_dir + "/" + _working_set_dir
	for regexp in regexps:
		command += " " + "\"" + regexp + "\""
	os.system(command)


# merge_working_set
#	Wrapper for merge-working-set.sh, which merges some working set back into
#	the main config directory.
#
# Arguments:
# _cfg_dir - the directory to merge into, relative to base of project.
# _working_set_dir - the working set, relative to base of project.

def merge_working_set(_cfg_dir, _working_set_dir):
	command = "sh" + " " + base_dir + "/config-generator/merge-working-set.sh" + " " + base_dir + "/" + _cfg_dir + " "  + base_dir + "/" + _working_set_dir
	os.system(command)


#######################
## MAIN ROUTINE

base_dir = str(sys.argv[1])
cfg_dir = str(sys.argv[2])

if not base_dir or not cfg_dir:
	sys.exit(-1)

test_working_dir = cfg_dir + "/pythtest"

new_working_set(cfg_dir,test_working_dir)
modify_working_set(test_working_dir, ['/bpred/c\\found you!'])
merge_working_set(cfg_dir, test_working_dir)
	