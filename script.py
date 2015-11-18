#!/usr/bin/env python
import subprocess
import shlex
import re

""" Script to call the simple scalar command """

# Adapted from a script written by Douglas Jordan <github.com/dwj300/>

BASE = "/home/software/simplesim/simplesim-3.0/sim-outorder"

commands = {
    "bzip2": " -config {machine}.cfg bzip2/bzip2_base.i386-m32-gcc42-nn bzip2/dryer.jpg",
    "hmmer": " -config {machine}.cfg hmmer/hmmer_base.i386-m32-gcc42-nn hmmer/bombesin.hmm",
    "mcf": " -config {machine}.cfg mcf/mcf_base.i386-m32-gcc42-nn mcf/inp.in",
    "sjeng": " -config {machine}.cfg sjeng/sjeng_base.i386-m32-gcc42-nn sjeng/test.txt",
    "milc": " -config {machine}.cfg milc/milc_base.i386-m32-gcc42-nn < milc/su3imp.in",
    "equake": " -config {machine}.cfg equake/equake_base.pisa_little < equake/inp.in"
}


def call_simplescalar():
    values = ["sim_IPC", "sim_total_insn", "ifq_occupancy", "ruu_occupancy", "lsq_occupancy"]
    pattern = re.compile(" [0-9.]+ ")

    for machine in range(1, 5):
        print "Machine: {0}".format(machine)
        print(","),
        for v in values:
            print("{0},".format(v)),
        print
        for k in commands.keys():
            v = commands[k]
            command = BASE + v
            print("{0},".format(k)),
            command = command.replace("{machine}", str(machine))
            args = shlex.split(command)
            if '<' in args:
                f_name = args[-1]
                args = args[:-2]
                p = subprocess.Popen(args, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=open(f_name))
            else:
                p = subprocess.Popen(args, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            cmd_out, cmd_err = p.communicate()
            lines = cmd_err.split('\n')
            for value in values:
                result = filter(lambda line: value in line, lines)[0]
                m = pattern.search(result)
                num = m.group().strip()
                print(str(num) + ","),
            print

if __name__ == '__main__':
    call_simplescalar()
