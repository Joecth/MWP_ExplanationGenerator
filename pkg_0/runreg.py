#!/usr/bin/env python
# -*- coding: UTF-8 -*-
import os
import shutil
import difflib
import popen2
import sys

IN_DIR = "./problems/"
ONLINE_CHI_DIR = "./problems/online/"
ONLINE_ENG_DIR = "./problems/english_qs/"
OUT_DIR = "./reg_output_new/"
GOLDEN_DIR = "./golden_eng/"
DIFF_LOG = "./diff_accr_new.log"
REPORT = "./report.log"
FILLER = "===================="
FILLER1 = "###"
FILLER2 = "^^^^^^^^^^^^^^^^^^^^"
global num_pass
num_pass = 0
global num_fail
num_fail = 0
print "Hello, world!"

def main():
    print "testing"
def diffRecorder(differ):
    if 0 == differ:
        result = "[Pass]"
        global num_pass 
        num_pass += 1
        return result
    else:
        result = "[Fail]"
        global num_fail 
        num_fail += 1
        return result

def test_foo(idx, DIR):
    case_idx = str(idx)
    if DIR == IN_DIR:
        sample = "tmp.trace.Sample-" + case_idx + ".xml"
    elif DIR == ONLINE_CHI_DIR:
        sample = case_idx + ".trace.xml"
    elif DIR == ONLINE_ENG_DIR:
        sample = case_idx + ".trace.xml"
    else:
        sys.exit(2)

    #O_SUFF = "   "
    O_SUFF = " -o "
    out_tmp = OUT_DIR + "case" + case_idx + ".xml"
    print out_tmp

    std_out, std_in = popen2.popen2("python3 __init__.py -i" + DIR + sample + O_SUFF + out_tmp)
    ostr = std_out.read()
    tree_log = "@@@@@@@@@@@@@@@@@  EG TREE : \n"
    tree_log += ostr

    diff_files = GOLDEN_DIR + "case" + case_idx + ".xml" + "  " + out_tmp 
    is_differ = os.system("diff -q " + diff_files)
    err_log = ""
    if 0 != is_differ:
        #err_log = os.system("diff " + diff_files)
        #err_log = 
       # pass
        # print ("aaaaaaaaaaaaaaaa")
        std_out, std_in = popen2.popen2("diff " + diff_files)
        #print ("std_out ::  ", std_out)
        ostr = std_out.read()
        #print (ostr)
        err_log += "@@@@@@@@@@@@@@@@@@ DIFF :\n"
        err_log += ostr
        ##print ("std_in  :: ", std_in.read())
    #if is_differ != 0
    #print is_differ
    result = diffRecorder(is_differ)

    #fp_o = open("out_new/out" + case_idx + ".xml", "w")
    msg = FILLER + "\tcase" + case_idx + "\t" + FILLER + "\n"
    msg += tree_log
    msg += FILLER1 + " end of EG Tree log " + "\n\n"
    if 0 != is_differ:
        msg += err_log
        msg += FILLER1 + "  end of err_log  " + "\n\n"
    msg += result
    msg += "\n"
    msg += FILLER2 + "\tend of case" + case_idx + "\t" + FILLER2 + "\n\n"
    
    fp_o.write(msg)
    fp_o.flush()
    #fp_o.close()
    print "\n" + msg + "\n"

def final_report():
    global num_pass
    global num_fail
    ret_str = "Pass: " + str(num_pass) + "\n" + "Fail: " + str(num_fail)
    print ret_str

def set_to_Chinese_env():
    os.environ["EG_Chinese"]="1" #os.system("export EG_Chinese=1")  on bash 
    print("EG_Chinese env on, value: " + os.environ["EG_Chinese"] + "\n")
    os.system("printenv |& grep EG_Chinese") #print(os.environ["EG_Chinese"])

def unset_Chinese_env(): 
    if os.environ["EG_Chinese"]:
        del os.environ["EG_Chinese"]
    print("EG_Chinese env off!")

if __name__ == '__main__':
    #num_pat = "[\d]+"
    #match_num = re.search(num_pat, lama)
    main()
    os.system("rm " + OUT_DIR + "*")
    fp_o = open(OUT_DIR + "out_report.xml", "w")

    cases = [1, 5, 6, 7, 8, 9, 17, 18, 19, 20, 21, 22] ## 75 Chinese cases
    set_to_Chinese_env()
    for case in cases: 
        test_foo(case, IN_DIR)
   
    print "\n\n\n" + FILLER2 + FILLER + FILLER2 + "\n"
    print "\t\tOnline Chinese website\t\t"
    set_to_Chinese_env()
    cases = ["EX_Diff1", "EX_Diff2", "EX1_Sub", "EX2_Sub", 
            "EX3_Add_Mul", "EX4_Add_Mul", "EX5_Mul_CmnDiv", 
            "EX6_Mul", "EX7_FlrDiv_CmnDiv", "EX8_FlrDiv_CmnDiv",
            "EX9_TVQ", "EX10_TVQ"]
    for case in cases:
        test_foo(case, ONLINE_CHI_DIR)

    print "\n\n\n" + FILLER2 + FILLER + FILLER2 + "\n"
    print "\t\tOnline English website\t\t"

    unset_Chinese_env()
    cases = ["EX11-pencil_and_eraser", "Dev-49-2",  "Sample-student", 
            "uwds-0001", "uwds-0001_changeunit", #"uwds-0001_changeunit_plural", 
            "Sample-1" ]
    for case in cases:
        test_foo(case, ONLINE_ENG_DIR)


    final_report()    
    fp_o.close()
# vim:set nu et ts=4 sw=4 cino=>4:    
