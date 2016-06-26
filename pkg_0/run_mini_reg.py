#!/usr/bin/env python
# -*- coding: UTF-8 -*-
import os
import popen2

def mini_foo():
    os.system('./run_uwcases_mini.py >& uw_mini.log')
    #print ("diff -q uwds{}_golden_000.log uw{}.log".format(idx, idx))
    is_differ = os.system("diff -q uwds_mini_golden_000.log uw_mini.log")
    err_log = ""

    if is_differ:
        print("Check Reg Fail!")
        print("Please diff uwds_mini_golden_000.log uw_mini.log\n")
    else:
        print("Reg_mini Pass!\n")

if __name__ == '__main__':
    #stdout, stdin = popen2.popen2('./run_uwcases_1.py')
    #foo(3)
###    for tmp in range(3):
###        idx = tmp + 1
###        print ('Dir%s :::'% idx)
    mini_foo()
