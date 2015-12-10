
#l_l1_blocksize 		= [8, 16, 32, 64]
#l_l2_blocksize 		= [64, 128, 256, 512, 1024]
l_l1_blocksize = [32,64]
l_l2_blocksize = [256,512,1024]

#l_l1_assoc 		= [1, 2, 4]
#l_l2_assoc		= [1, 2, 4, 8, 16]
l_l1_assoc = [4]
l_l2_assoc = [4]

#l_bpred			= ['bimod', 'taken', 'nottaken', '2lev']
l_bpred = ['2lev']

#l_decode_width 		= [1, 2, 4, 8, 16]
l_decode_width = [4]

# Note: issue width for static is 1,2,4; for dynamic is 2,4,8.
#l_issue_width		= [1, 2, 4, 8]
l_issue_width = [4]

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
l_issue_inorder = ['true','false']
