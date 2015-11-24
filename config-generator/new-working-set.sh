#!/bin/bash

# Script to create a new "working set" - i.e., a copy of all current configs
# which we can modify with different parameters. The intended use is:
#
# script calls new-working-set.sh to copy all current cfgs into a temporary
# 	directory (and give them random names).
# script calls modify-working-set.sh to give a sed-style regexp replacement
#	string which will be applied to all files in the working set.
# script calls merge-working-set.sh which copies the working set into the 
#	main cfgs directory.
#
# Arguments:
# $1 - the abs. path of the base of the final project.
# $2 - the configs directory, relative to the base in $1
# $3 - the temporary working directory to copy to (doesn't have to exist)
#	again, relative to the base in $1.

base_dir=$1
cfg_dir=$2
working_set_dir=$3

mkdir "$base_dir"/"$working_set_dir"

# Copy each file in with a random name.
for file in "$base_dir"/"$cfg_dir"/*.cfg; do
	new_filename=$(python "$base_dir"/utils/random_filename.py)	
 	cp "$file" "$base_dir"/"$working_set_dir"/"$new_filename".cfg
done

exit 0
