if [ -z "$1" ]
	then
		echo "Please supply the folder name to drop the sim results into as the first argument."
		exit
fi

if [ -z "$2" ]
	then
		echo "Please supply a config file as the second argument."
		exit
fi


# bzip2
mkdir -p bzip2/$1
cd bzip2/$1
$SIMPLESIM/simplesim-3.0/sim-outorder -config ../../$2 ../bzip2_base.i386-m32-gcc42-nn ../dryer.jpg
cd ../..

# mcf
mkdir -p mcf/$1
cd mcf/$1
$SIMPLESIM/simplesim-3.0/sim-outorder -config ../../$2 ../mcf_base.i386-m32-gcc42-nn ../inp.in
cd ../..

# hmmer
mkdir -p hmmer/$1
cd hmmer/$1
$SIMPLESIM/simplesim-3.0/sim-outorder -config ../../$2 ../hmmer_base.i386-m32-gcc42-nn ../bombesin.hmm
cd ../..

# sjeng
mkdir -p sjeng/$1
cd sjeng/$1
$SIMPLESIM/simplesim-3.0/sim-outorder -config ../../$2 ../sjeng_base.i386-m32-gcc42-nn ../test.txt
cd ../..

# milc
mkdir -p milc/$1
cd milc/$1
$SIMPLESIM/simplesim-3.0/sim-outorder -config ../../$2 ../milc_base.i386-m32-gcc42-nn < ../su3imp.in
cd ../..

# equake
mkdir -p equake/$1
cd equake/$1
$SIMPLESIM/simplesim-3.0/sim-outorder -config ../../$2 ../equake_base.pisa_little < ../inp.in 
cd ../.. 
