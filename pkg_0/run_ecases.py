#!/usr/bin/env python
# -*- coding: UTF-8 -*-
import os
import shutil
import difflib
import popen2
NUM = 8 ## amount of testing cases
IN_DIR = "./demo_cases/tmp.edemo.out.20160413/"
FILLER = "===================="
FILLER1 = "###"
FILLER2 = "^^^^^^^^^^^^^^^^^^^^"

def run_eg_cases(ith):
    #print("\n------------------ Start of Case " +  ith +  " ---------------- \n")
    cmd = "python3 __init__.py -i " + IN_DIR + "ex" + str(ith) + ".trace.xml" \
                           + " -l " + IN_DIR + "ex" + str(ith) + ".lft.xml" \
                           + " -s " + IN_DIR + "ex" + str(ith) + ".stc.xml"
    stdout, stdin = popen2.popen2(cmd)
    ostr = stdout.read()
    #print("\n~~~~~~~~~~~~~~~~~~ End of Case " + ith + "~~~~~~~~~~~~~~~~~~~~~\n")

    #msg = filler
    msg = FILLER + "\tcase" + ith + "\t" + FILLER + "\n"
    msg += ostr
    msg += FILLER2 + "\tend of case" + ith + "\t" + FILLER2 + "\n\n"
    print "\n" + msg + "\n"

if __name__ == '__main__':
    cases = range(1, NUM+1)
    for ith in cases:
        tmp = "0%1s"% ith
        #print(tmp)
        run_eg_cases(tmp)
