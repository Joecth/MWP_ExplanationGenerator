#!/usr/bin/env python
# -*- coding: UTF-8 -*-
import os
import popen2

def foo(idx):
    os.system('./run_uwcases_{}.py >& uw{}.log'.format(idx, idx))
    #print ("diff -q uwds{}_0505_000.log uw{}.log".format(idx, idx))
    is_differ = os.system("diff -q uwds{}_0505_000.log uw{}.log".format(idx, idx))
    err_log = ""

    if is_differ:
        print("Check Reg Fail!")
        print("Please diff uwds{}_0505_000.log uw{}.log\n".format(idx, idx))
    else:
        print("Reg%s Pass!\n" % idx)

if __name__ == '__main__':
    #stdout, stdin = popen2.popen2('./run_uwcases_1.py')
    #foo(3)
    for tmp in range(3):
        idx = tmp + 1
        print ('Dir%s :::'% idx)
        foo(idx)

