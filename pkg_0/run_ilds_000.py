#!/usr/bin/env python
# -*- coding: UTF-8 -*-
import os
import popen2

def foo(idx):
    os.system('./run_ilds_{}.py >& il{}.log'.format(idx, idx))
    #print ("diff -q ilds{}_golden_000.log il{}.log".format(idx, idx))
    is_differ = os.system("diff -q ilds{}_golden_000.log il{}.log".format(idx, idx))
    err_log = ""

    if is_differ:
        print("Check Reg Fail!")
        print("Please diff ilds{}_golden_000.log il{}.log\n".format(idx, idx))
    else:
        print("Reg%s Pass!\n" % idx)

if __name__ == '__main__':
    #stdout, stdin = popen2.popen2('./run_ilds_1.py')
    #foo(3)
    #foo(1)
    for tmp in range(1):
        idx = tmp + 4 
        print ('Dir mini_%s :::'% idx)
        foo(idx)

