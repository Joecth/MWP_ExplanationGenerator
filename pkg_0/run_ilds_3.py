#!/usr/bin/env python
# -*- coding: UTF-8 -*-
import os
import shutil
import difflib
import popen2
import re

NUM = 8 ## amount of testing cases
#IN_DIR = "./demo_cases/tmp.edemo.out.20160413/"
#IN_DIR_DS1 = "./demo_cases/task.UWDS.20160407/data.ENG.UW.DS1.new/"
IN_DIR_DS1 = "./demo_cases/IllinoisCases/data.ENG.IL.ILDS.new/mini_3"
#IN_DIR_DS1_SMALL = "./demo_cases/task.UWDS.20160407/data.ENG.UW.DS1.small/"
IN_DIR_DS1_SMALL = "./demo_cases/IllinoisCases/data.ENG.IL.ILDS.new.small/"

#IN_DIR_DS1 = IN_DIR_DS1_SMALL
FILLER = "===================="
FILLER1 = "###"
FILLER2 = "^^^^^^^^^^^^^^^^^^^^"

if __name__ == '__main__':
##    for ith in cases:
##        tmp = "0%1s"% ith
##        #print(tmp)
##        run_eg_cases(tmp)
    pattern = ".*lft.xml"

    for root, _, files in os.walk(IN_DIR_DS1):
    #print("root: " + root)
        for f in files:
            #print("file: " + f)
            match_file = re.search(pattern, f)
            if match_file:
                num = match_file.group()[:-8]
    
                t_file_name = num + ".trace.xml" # name of trace file
                #print("trace name : " + t_file_name)
                t_full = os.path.join(root, t_file_name)
                #print("trace full : " + t_full)
    
                l_file_name = num + ".lft.xml" #name of lft file
                #print("lft name : " + l_file_name)
                l_full = os.path.join(root, l_file_name)
                #print("lft full : " + l_full)
    
                s_file_name = num + ".stc.xml" #name of stc file
                #print("stc name : " + s_file_name )
                s_full = os.path.join(root, s_file_name)
                #print("stc full : " + s_full)
                
                cmd = "python3 __init__.py -i " + t_full\
                                       + " -l " + l_full \
                                       + " -s " + s_full

                #print("\n------------------ Start of Case " +  ith +  " ---------------- \n")
                ret_str = cmd + "\n"

                stdout, stdin = popen2.popen2(cmd)
                ostr = stdout.read()
                ret_str += ostr
                #print("\n~~~~~~~~~~~~~~~~~~ End of Case " + ith + "~~~~~~~~~~~~~~~~~~~~~\n")
            
                #msg = filler
                msg = FILLER + "\tstart of case : " + num + "\t" + FILLER + "\n"
                msg += ret_str
                msg += FILLER2 + "\tend of case : " + num + "\t" + FILLER2 + "\n\n"
                print "\n" + msg + "\n"
