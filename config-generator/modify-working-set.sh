# modify-working-set.sh
# 
# Arguments:
# $1 - the working set location.
# $2... - sed-style replacement strings to apply to the files. 
#	e.g. /[text to find]/c\\[replacement line]
#	NOTE the double backslash needed to escape the slash.
#	not sure if this is right, and it's messy.

working_set_dir=$1;

for regexp in "${@:2}"; do
	sed -i -e "$regexp" "$working_set_dir"/*
done
