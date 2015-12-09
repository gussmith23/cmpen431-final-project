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
import itertools  # for itertools.product.


#######################
## Fields

# These keys are used to lookup a string which is then passed
#	to sed for find-and-replace.
# The values should each map to a single line; i.e., if we use this
#	dictionary to find-and-replace a setting, we won't overwrite
#	multiple lines.
ss_settings = {
	'ifqsize': 	"-fetch:ifqsize",
	'fspeed': 	"-fetch:speed",
	'fmplat':	"-fetch:mplat",
	'bpred':	"-bpred ",		# This one may be an issue...
	'ras':		"-bpred:ras",
	'dwidth':	"-decode:width",
	'iwidth':	"-issue:width",
	'inorder':	"-issue:inorder",
	'wrongpath':	"-issue:wrongpath",
	'ruusize':	"-ruu:size",
	'lsqsize':	"-lsq:size",
	'ialu':		"-res:ialu",
	'imult':	"-res:imult",
	'fpalu':	"-res:fpalu",
	'fpmult':	"-res:fpmult",
	'memport':	"-res:memport",
	'il1':		"-cache:il1 ",
	'il2':		"-cache:il2 ",
	'dl1':		"-cache:dl1 ",
	'dl2':		"-cache:dl2 ",
	'ul2':		"-cache:dl2 ", # note this
	'itlb':		"-tlb:itlb",
	'dtlb':		"-tbl:dtlb",
	'il1lat':	"-cache:il1lat",
	'il2lat':	"-cache:il2lat",
	'dl1lat':	"-cache:dl1lat",
	'dl2lat':	"-cache:dl2lat",
	'memlat':	"-mem:lat",
	'memwidth':	"-mem:width",
	'redir':	"-redir:sim"
}


## POSSIBLE SETTING VALUES
# (l stands for list. i'm not good at naming things)

l_l1_blocksize 		= [8, 16, 32, 64]
l_l2_blocksize 		= [64, 128, 256, 512, 1024]

l_l1_assoc 		= [1, 2, 4]
l_l2_assoc		= [1, 2, 4, 8, 16]

l_bpred			= ['bimod', 'taken', 'nottaken', '2lev']

l_decode_width 		= [1, 2, 4, 8, 16]

# Note: issue width for static is 1,2,4; for dynamic is 2,4,8.
l_issue_width		= [1, 2, 4, 8]

# Fetch speed ratios - this should probably always be 4
l_fetch_speed		= [1,2,3,4]

l_imult 		= range(1, 2*8+1)
l_ialu			= l_imult
l_fpmult 		= l_imult
l_fpalu			= l_imult

l_ras			= [8, 16]

l_btb_sets 		= [512, 1024]

l_ruusize 		= [2, 4, 8, 16, 32, 64]

l_lsqsize		= [2, 4, 8, 16, 32]

l_issue_inorder 	= ['true', 'false']


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

def new_working_set(_base_dir, _cfg_dir, _working_set_dir):
	command = "sh" + " " + _base_dir + "/config-generator/new-working-set.sh" + " "  + _base_dir + " " + _cfg_dir + " " + _working_set_dir
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

def modify_working_set(_base_dir, _working_set_dir, regexps):
	command = "sh" + " " + _base_dir + "/config-generator/modify-working-set.sh" + " "  + _base_dir + "/" + _working_set_dir
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

def merge_working_set(_base_dir, _cfg_dir, _working_set_dir):
	command = "sh" + " " + _base_dir + "/config-generator/merge-working-set.sh" + " " + _base_dir + "/" + _cfg_dir + " "  + _base_dir + "/" + _working_set_dir
	os.system(command)


## HELPER FUNCTIONS

# 
# Arguments:
# name: string with one of the following vals:
#	il1, il2, dl1, dl2, ul2
#
# see https://www.doc.ic.ac.uk/~phjk/AdvancedCompArchitecture/2001-02/Lectures/Ch03-Caches/node31.html
#	for more documentation on cache settings.

def create_cache_change_regex(name, nsets, bsize, assoc, repl):
	setting_string = ss_settings[name]
	return "/" + setting_string + "/c\\" + setting_string + " " + name + ":" + str(nsets) + ":" + str(bsize) + ":" + str(assoc) + ":" + repl


# create_ss_setting_change_regex 
# Arguments:
# name: setting name to be changed

def create_setting_change_regex(name, vals):
	setting_string = ss_settings[name]
	regex =  "/" + setting_string + "/c\\" + setting_string 
	for val in vals:
		regex += " " + str(val)
	return regex


#######################
## MAIN ROUTINE

def config_generator(base_dir, cfg_dir,
				_l_l1_blocksize = l_l1_blocksize,
				_l_l2_blocksize = l_l2_blocksize,
				_l_l1_assoc	= l_l1_assoc,   
				_l_l2_assoc	= l_l2_assoc,    
				_l_bpred	= l_bpred,	      
				_l_decode_width	= l_decode_width,
				_l_issue_width	= l_issue_width,
				_l_fetch_speed 	= l_fetch_speed,
				_l_imult	= l_imult,
				_l_ialu		= l_ialu,
				_l_fpmult	= l_fpmult,
				_l_fpalu	= l_fpalu,
				_l_ras		= l_ras,
				_l_btb_sets	= l_btb_sets,
				_l_ruusize	= l_ruusize,
				_l_lsqsize	= l_lsqsize,
				_l_issue_inorder= l_issue_inorder):


	# Check for valid input.
	if not base_dir or not cfg_dir:
		sys.exit(-1)


	product_counter = 0
	total_products = len(_l_l1_blocksize)*len(_l_l2_blocksize)*len(_l_l1_assoc)*len(_l_l2_assoc)\
				*len(_l_bpred)*len(_l_decode_width)

	for product in itertools.product( _l_l1_blocksize,	#0 
					_l_l2_blocksize, 	#1
					_l_l1_assoc, 		#2
					_l_l2_assoc, 		#3
					_l_bpred, 		#4
					_l_decode_width,	#5
					_l_issue_width,		#6
					_l_fetch_speed,		#7
					_l_imult,		#8
					_l_ialu,		#9
					_l_fpmult,		#10
					_l_fpalu,		#11
					_l_ras,			#12
					_l_btb_sets,		#13
					_l_ruusize,		#14
					_l_lsqsize,		#15
					_l_issue_inorder):	#16
		
		## Get values from product.

		l1_block_size = product[0]
		l2_block_size = product[1]

		l1_assoc = product[2]
		l2_assoc = product[3]

		l1_size = 1024*8
		l2_size = 2048*16*2

		bpred = product[4]
		
		decode_width = product[5]

		issue_width = product[6]

		fetch_speed = product[7]

		imult = product[8]
		ialu = product[9]
		fpmult = product[10]
		fpalu = product[11]
		
		ras = product[12]
		
		btb_sets = product[13]

		ruusize = product[14]

		lsqsize = product[15]

		inorder = product[16]
		
		
		## Set values based on values from product.
		
		# ifq size
		ifq_size = l1_block_size/8

		# l1 latency	
		l1_lat = 1
		if l1_block_size == 8:
			l1_lat = 1
		elif l1_block_size == 16:
			l1_lat = 2
		elif l1_block_size == 32:
			l1_lat = 3
		elif l1_block_size == 64:
			l1_lat = 4
		
		if l1_assoc == 2:
			l1_lat += 1
		elif l1_assoc == 4:
			l1_lat += 2

		# l2 latency
		l2_lat = 5
		if l2_block_size == 64:
			l2_lat = 5
		elif l2_block_size == 128:
			l2_lat = 6
		elif l2_block_size == 256:
			l2_lat = 7
		elif l2_block_size == 512:
			l2_lat = 8
		elif l2_block_size == 1024:
			l2_lat = 9	

		if l2_assoc == 1:
			l2_lat += -1
		elif l2_assoc == 4:
			l2_lat += 1
		elif l2_assoc == 8:
			l2_lat += 2
		elif l2_assoc == 16:
			l2_lat += 3


		## Check values.

		if l1_block_size*2 > l2_block_size:
			continue
		
		# decode:width less than or equal to fetch:ifqsize
		if decode_width > ifq_size:
			continue

		# imult+ialu <= 2*issue_width (same for fpmult/alu)
		if imult + ialu > 2*issue_width:
			continue
		if fpmult + fpalu > 2*issue_width:
			continue
		
		# ruusize no more than 8 times issue_width
		if ruusize > 8*issue_width:
			continue

		# lsqsize no more than 4 times issue_width
		if lsqsize > 4*issue_width:
			continue

		# issue widths are 1,2,4 for static, 2,4,8 for dynamic
		if inorder == "true" and issue_width == 8:
			continue
		if inorder == "false" and issue_width == 1:
			continue

		## Create working set.
		working_set_dir = cfg_dir + "/tmp/"
		new_working_set(base_dir, cfg_dir, working_set_dir)

		## Create modifications.
		regexes = []
		
		# l1, l2.
		regexes.append(create_cache_change_regex("il1",l1_size/(l1_block_size*l1_assoc), l1_block_size,l1_assoc,"r"))
		regexes.append(create_cache_change_regex("dl1",l1_size/(l1_block_size*l1_assoc), l1_block_size,l1_assoc,"r"))
		regexes.append(create_cache_change_regex("ul2",l2_size/(l2_block_size*l2_assoc), l2_block_size,l2_assoc,"r"))
		
		# ifq size
		regexes.append(create_setting_change_regex("ifqsize", [ifq_size]))

		# l1 latencies	
		regexes.append(create_setting_change_regex("il1lat", [l1_lat]))
		regexes.append(create_setting_change_regex("dl1lat", [l1_lat]))

		# ul2 latency
		regexes.append(create_setting_change_regex("il2lat", [l2_lat]))
		regexes.append(create_setting_change_regex("dl2lat", [l2_lat]))

		# bpred
		regexes.append(create_setting_change_regex("bpred", [bpred]))

		# decode_width
		regexes.append(create_setting_change_regex("dwidth", [decode_width]))

		# issue_width
		regexes.append(create_setting_change_regex("iwidth", [issue_width]))
		
		# fetch speed
		regexes.append(create_setting_change_regex("fspeed", [fetch_speed]))

		# resource sizes
		regexes.append(create_setting_change_regex("imult", [imult]))
		regexes.append(create_setting_change_regex("ialu", [ialu]))
		regexes.append(create_setting_change_regex("fpmult", [fpmult]))
		regexes.append(create_setting_change_regex("fpalu", [fpalu]))

		# ras
		regexes.append(create_setting_change_regex("ras", [ras]))

		# TODO btb

		
		#ruusize
		regexes.append(create_setting_change_regex("ruusize",[ruusize]))

		# lsqsize
		regexes.append(create_setting_change_regex("lsqsize", [lsqsize]))

		# inorder
		regexes.append(create_setting_change_regex("inorder", [inorder]))
		

		## Create a name for the output!
		# Note: at the moment this is not used, as we no longer redir 
		#	to file.
		out_name = str(l1_block_size) + "_" \
			+ str(l2_block_size) + "_" \
			+ str(l1_assoc) + "_" \
			+ str(l2_assoc) + ".out"

		regexes.append(create_setting_change_regex("redir", [out_name]))


		## Modify working set.
		modify_working_set(base_dir, working_set_dir, regexes)


		## Merge.
		merge_working_set(base_dir, cfg_dir, working_set_dir)

		## Update product counter.
		product_counter += 1
		print("Progress: [" + str(product_counter) + "/" + str(total_products) + "]")

