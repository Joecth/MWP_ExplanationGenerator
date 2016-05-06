0. cd pkg_0

### Execute:
1. python3 __init__.py -i [input.trace.xml] -o [out.xml] 
    // default output: output.xml,
    // log files: raw_tree.xml, build_tree.log.xml
 
### Regression:
Reg 1)
    1. ./runreg.py     
    // script, run under shell; popen2 package cannot be found in PyCharm
    2. vi ./reg_output_new/report.xml
    // to see the diff of all cases in regression this run
Reg 2)
    ./run_uwds_0.py
