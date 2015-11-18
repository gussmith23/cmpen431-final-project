for benchmark in bzip2 milc sjeng mcf hmmer equake
do
	cd $benchmark/hw05
	
	echo "$benchmark"...
	echo $benchmark > "$benchmark".out	
	
	# pretty lame workaround. find a way to exclude "$benchmark".out.
	for filename in hw*
	do
		echo "$filename"...
		echo $filename >> "$benchmark".out
		cat $filename | egrep '(sim_IPC|sim_total_insn)' >> "$benchmark".out
		echo >> "$benchmark".out		
	done

	cd ../.. 

done
