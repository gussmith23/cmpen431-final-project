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
# $1 - the configs directory.
# $2 - the temporary working directory to copy to (doesn't have to exist)

cfg_dir=$1
working_set_dir=$2

mkdir "$working_set_dir"

# Copy each file in with a random name.
for file in "$cfg_dir"/*; do
	cp "$file" "$working_set_dir"/$(cat /dev/urandom | tr -dc 'a-zA-Z0-9' | fold -w 32 | head -n 1).cfg
done
