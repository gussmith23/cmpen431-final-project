# merge-working-set.sh
#

cfg_dir=$1
working_set_dir=$2

mkdir "$cfg_dir"
mv "$working_set_dir"/* "$cfg_dir"
rm -rf "$working_set_dir"
