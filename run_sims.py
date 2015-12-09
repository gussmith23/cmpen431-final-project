import os
execfile("config-generator/config-generator.py")
execfile("simulation-runner/simulation-runner.py")
# this is messy: import parse_output.
execfile(os.getcwd() + "/output_parser/output_parser_export.py")

## First: generate configs.

# Settings.

# The settings and their values.
# Any settings not set will cause the config generator to include ALL possible values for the setting.

#l_l1_blocksize 		= [8, 16, 32, 64]
#l_l2_blocksize 		= [64, 128, 256, 512, 1024]
#l_l1_assoc 			= [1, 2, 4]
#l_l2_assoc			= [1, 2, 4, 8, 16]
#l_bpred			= ['bimod', 'taken', 'nottaken', '2lev']
#l_decode_width 		= [1, 2, 4, 8, 16]

l_l1_blocksize = [16]
l_l2_blocksize = [64,128,256,512,1024]
l_l1_assoc = [2]
l_l2_assoc = [4]
l_bpred = ['2lev']
l_decode_width = [4]

# Note: assumes we're in the root of the project dir!
config_generator(os.getcwd(), "output", 
				_l_l1_blocksize = l_l1_blocksize,
				_l_l2_blocksize = l_l2_blocksize,
				_l_l1_assoc	= l_l1_assoc,   
				_l_l2_assoc	= l_l2_assoc,    
				_l_bpred	= l_bpred,	      
				_l_decode_width	= l_decode_width)



## Run sims.
simulation_runner(os.getcwd(),"output","output/out")

