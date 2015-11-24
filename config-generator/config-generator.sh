# $1 - the directory containing the cfgs.
# $2-onward - the sed replacement regex. should be of the
# 	form "/[searchtext]/c\[replacement]"
function spawn_new_cfgs {
	mkdir "$1"/tmp
	cp "$1"/*.cfg "$1"/tmp
	for regexp in "${@:2}"; do
		sed -i -e "$regexp" "$1"/tmp/*
	done

	for file in "$1"/tmp/*; do
		mv "$file" "$1"/tmp/$(cat /dev/urandom | tr -dc 'a-zA-Z0-9' | fold -w 32 | head -n 1).cfg
	done

	mv "$1"/tmp/* "$1"
	rm -rf "$1"/tmp
}



# Cache settings
for blocksize in 8 16 32 64; do
	# il1 block size = dl1 block size = ifq siz
	echo ""	
done

spawn_new_cfgs $1 "/bpred/c\\LOL"


