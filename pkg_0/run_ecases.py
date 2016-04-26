#!/usr/bin/env python
# -*- coding: UTF-8 -*-
import os
import shutil
import difflib
import popen2
NUM = 8 ## amount of testing cases
IN_DIR = "./demo_cases/tmp.edemo.out.20160413/"

def run_eg_cases(ith):
    print("\nCase " +  ith +  ": \n")
    cmd = "python3 __init__.py -i " + IN_DIR + "ex" + str(ith) + ".trace.xml" \
                           + " -l " + IN_DIR + "ex" + str(ith) + ".lft.xml" \
                           + " -s " + IN_DIR + "ex" + str(ith) + ".stc.xml"
    os.system(cmd)

if __name__ == '__main__':
    cases = range(1, NUM+1)
    for ith in cases:
        tmp = "0%1s"% ith
        #print(tmp)
        run_eg_cases(tmp)
