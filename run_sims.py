import os
execfile("config-generator/config-generator.py")
execfile("simulation-runner/simulation-runner.py")
# this is messy: import parse_output.
execfile(os.getcwd() + "/output_parser/output_parser_export.py")

## First: generate configs.

# Settings.

### The settings and their values.
# Any settings not set will cause the config generator to include ALL possible values for the setting.
# Instructions:
# 	Change these values to determine which configs of simplescalar will be run.
#	Commented out code above each line lists all possible values for a setting.
#	on the line below it, assign the l_[some_setting] variable to some subset of
#	the values listed in the commented line.

#l_l1_blocksize 		= [8, 16, 32, 64]
#l_l2_blocksize 		= [64, 128, 256, 512, 1024]
l_l1_blocksize = [8,16,32,64]
l_l2_blocksize = [64,128,256,512,1024]

#l_l1_assoc 		= [1, 2, 4]
#l_l2_assoc		= [1, 2, 4, 8, 16]
l_l1_assoc = [1,2,4]
l_l2_assoc = [1,2,4,8,16]

#l_l1_size			= [8, 16, 32, 64]
#l_l2_size			= [64, 128, 256, 512, 1024] THESE ARE KILOBYTES!
l_l1_size			= [8,16,32,64]
l_l2_size			= [64,128,256,512,1024]

#l_bpred			= ['bimod', 'taken', 'nottaken', '2lev']
l_bpred = ['bimod']

#l_decode_width 		= [1, 2, 4, 8, 16]
l_decode_width = [1,4,16]

# Note: issue width for static is 1,2,4; for dynamic is 2,4,8.
#l_issue_width		= [1, 2, 4, 8]
l_issue_width = [4,8]

# Fetch speed ratios - this should probably always be 4
#l_fetch_speed		= [1,2,3,4]
l_fetch_speed = [4]

#l_imult 		= range(1, 2*8+1)
#l_ialu			= l_imult
#l_fpmult 		= l_imult
#l_fpalu			= l_imult
# NOTE: these values can also be set to just "max", to be set to their max possible
#	values. if one of a pair is max, the other should also be max (for now.)
l_imult = ["max"]
l_ialu = ["max"]
l_fpmult = ["max"]
l_fpalu = ["max"]


#l_ras			= [8, 16]
l_ras = [16]

#l_btb_sets 		= [512, 1024]
l_btb_sets = [1024]

#l_ruusize 		= [2, 4, 8, 16, 32, 64] or ["max"]
l_ruusize = ["max"]

#l_lsqsize		= [2, 4, 8, 16, 32] or ["max"]
l_lsqsize = ["max"]

#l_issue_inorder 	= ['true', 'false']
l_issue_inorder = ['false']

#l_l1_repl		= ['l','r']
#l_l2_repl		= ['l','r']
l_l1_repl		= ['l']
l_l2_repl		= l_l1_repl

# Note: assumes we're in the root of the project dir!
config_generator(os.getcwd(), "output", 
				doubling = False,
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
				_l_issue_inorder= l_issue_inorder,
				_l_l1_repl	= l_l1_repl,
				_l_l2_repl	= l_l2_repl,
				_l_l1_size	= l_l1_size,
				_l_l2_size	= l_l2_size)



## Run sims.
simulation_runner(os.getcwd(),"output","output/out")

