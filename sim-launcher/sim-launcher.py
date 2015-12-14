# Simplesim launcher / automation script
# Written by Ethan Goff (github.com/ethangoff)
# Input: Directory containing configuration files, directory to place simulation output files.
# Output: SimpleScalar simulation output files.

import sys
import argparse
import glob
import shlex
from subprocess import PIPE, Popen

# Quick switch for silencing all output (not sure if you can override built-in functions like print)
def printI(msg, skip = False):
    if not skip:
        print msg


def main(SimpleSimLocation, SourceConfigsDirectory, OutputDirectory):
    # Define sim tasks
    commands = {
        "bzip2": " -config {config}.cfg bzip2/bzip2_base.i386-m32-gcc42-nn bzip2/dryer.jpg",
        "hmmer": " -config {config}.cfg hmmer/hmmer_base.i386-m32-gcc42-nn hmmer/bombesin.hmm",
        "mcf": " -config {config}.cfg mcf/mcf_base.i386-m32-gcc42-nn mcf/inp.in",
        "sjeng": " -config {config}.cfg sjeng/sjeng_base.i386-m32-gcc42-nn sjeng/test.txt",
        "milc": " -config {config}.cfg milc/milc_base.i386-m32-gcc42-nn < milc/su3imp.in",
        "equake": " -config {config}.cfg equake/equake_base.pisa_little < equake/inp.in"
    }

    # Iterate over all .cfg files
    for configFile in glob.glob(SourceConfigsDirectory + '*.cfg'):
        printI("Using " + configFile)

        for task in commands.keys():
            taskArgs = commands[task]
            command = (SimpleSimLocation + taskArgs)replace("{config}", str(configFile))
            processHost = shlex.split(command)
            if '<' in processHost:
                f_name = processHost[-1]
                processHost = processHost[:-2]
                p = subprocess.Popen(processHost, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=open(f_name))
            else:
                p = subprocess.Popen(processHost, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            p_std_out, p_std_err = p.communicate()




# Entry Point
parser = argparse.ArgumentParser()
parser.add_argument("--SS_path", help="An absoloute path to the simple scalar executable (i.e. <dir>/sim-outorder) ")
parser.add_argument("--src_cfg_dir", help="An absoloute path (with a trailing /) to a directory containing configuration files to launch simplescalar with (with names of the form *.cfg) ")
parser.add_argument("--out_dest_dir", help="An absoloute path (with a trailing /) to a directory where output files will be placed (with names of the form *.out) ")
args = parser.parse_args()
if args.SS_path and args.src_cfg_dir and args.out_dest_dir:
    if args.src_cfg_dir[-1:] != "/" or args.src_cfg_dir[-1:] != "/" :
        print "Both directory arguments must end with a trailing /"
    else:
        main(args.src_cfg_dir, args.out_dest_dir)
else:
    print "This script must be called with three arguments: '--SS_path <path>', '--src_cfg_dir <dir>', and '--out_dest_dir <dir>'. Call with -h argument for help."
