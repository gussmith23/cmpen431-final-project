# Simplesim output parser
# Written by Ethan Goff (github.com/ethangoff)
# Input: Directory containing output files, directory to place simulation output files.
# Output: A csv file containing

import sys
import argparse
import glob
import shlex
from subprocess import PIPE, Popen

# Quick switch for silencing all output (not sure if you can override built-in functions like print)
def printI(msg, skip = False):
    if not skip:
        print msg


def performance(IPC, ClockRate, InstructionCount)


def main(SourceDirectory, OutputDirectory):
    pattern = re.compile(" [0-9.]+ ")

    # Iterate over all .cfg files
    for outputRecord in glob.glob(SourceDirectory + '*.out'):
        with open(outputRecord) as outputRecordFile:
            printI("Parsing " + outputRecord)
            output = outputRecord + "\n"
            output = output + "sim_IPC, sim_total_insn, performance"

            lines = outputRecordFile.readlines()

            IPCWithTag = filter(lambda line: "sim_IPC" in line, lines)[0]
            IPC = pattern.search(IPCWithTag).group().strip()
            output = output + (str(num) + ",")

            totalInstrWithTag = filter(lambda line: "sim_total_insn" in line, lines)[0]
            totalInstr = pattern.search(totalInstrWithTag).group().strip()
            output = output + (str(num) + ",")

            clockRate = 100;

            fixed_perf = performance(IPC, clockRate, totalInstr)
            floating_perf = performance(IPC, clockRate, totalInstr)


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
